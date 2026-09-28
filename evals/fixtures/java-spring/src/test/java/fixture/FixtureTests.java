package fixture;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.RollbackException;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.atomic.AtomicInteger;
import org.hibernate.SessionFactory;
import org.hibernate.stat.Statistics;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class OrderDesiredContractTest {
  @Autowired MockMvc mvc;
  @Autowired OrderRepository repository;
  @BeforeEach void clean() { repository.deleteAll(); }
  @Test void nonexistentOrderMustReturn404AtMvcBoundary() throws Exception {
    mvc.perform(get("/orders/{id}", 999L)).andExpect(status().isNotFound());
  }
}

@SpringBootTest
@AutoConfigureMockMvc
class HttpSerializationContractTest {
  @Autowired MockMvc mvc;
  @Test void jsonPropertyDefinesWireNameInsteadOfJavaComponentName() throws Exception {
    mvc.perform(get("/contracts/customer"))
      .andExpect(status().isOk())
      .andExpect(jsonPath("$.customerName").value("Ada"))
      .andExpect(jsonPath("$.name").doesNotExist());
  }
  @Test void beanValidationIsObservedAtMvcBoundary() throws Exception {
    mvc.perform(post("/contracts/orders")
        .contentType(MediaType.APPLICATION_JSON)
        .content("{\"label\":\"\"}"))
      .andExpect(status().isBadRequest());
  }
}

@SpringBootTest
class SpringTransactionSemanticsTest {
  @Autowired OrderRepository repository;
  @Autowired AuditRepository audits;
  @Autowired TransactionScenarioService scenarios;
  @Autowired TransactionProbe probe;
  @Autowired OuterTransactionService outer;
  @BeforeEach void clean() { audits.deleteAll(); repository.deleteAll(); }
  @Test void flushBeforeRuntimeExceptionDoesNotProveCommit() {
    assertThrows(IllegalStateException.class, () -> scenarios.saveFlushThenRuntimeFailure(101L));
    assertFalse(repository.existsById(101L));
  }
  @Test void checkedExceptionCommitsByDefaultUnlessRollbackRulesChange() {
    assertThrows(TransactionScenarioService.CheckedFixtureException.class, () -> scenarios.saveFlushThenCheckedFailure(202L));
    assertTrue(repository.existsById(202L));
  }
  @Test void selfInvocationDoesNotCrossDefaultTransactionalProxy() {
    assertFalse(probe.outerCallsInner());
    assertTrue(probe.innerTransactional());
  }
  @Test void requiresNewCanCommitEvenWhenOuterTransactionRollsBack() {
    assertThrows(IllegalStateException.class, () -> outer.writeThenFail(303L, 404L));
    assertFalse(repository.existsById(303L));
    assertTrue(audits.existsById(404L));
  }
}

@SpringBootTest(properties = "spring.jpa.properties.hibernate.generate_statistics=true")
class JpaBehaviorTest {
  @Autowired AuthorRepository authors;
  @Autowired AuthorQueryService queryService;
  @Autowired InventoryRepository inventory;
  @Autowired EntityManagerFactory emf;
  @BeforeEach void clean() { inventory.deleteAll(); authors.deleteAll(); }

  @Test void nPlusOneMustBeMeasuredAtQueryBoundary() {
    for (long i = 1; i <= 3; i++) {
      AuthorEntity author = new AuthorEntity(i, "a" + i);
      author.addBook(new BookEntity(100 + i, "b" + i));
      authors.save(author);
    }
    authors.flush();
    Statistics stats = emf.unwrap(SessionFactory.class).getStatistics();
    stats.setStatisticsEnabled(true);
    stats.clear();
    assertEquals(3, queryService.countBooks(false));
    long statementsWithNPlusOne = stats.getPrepareStatementCount();
    stats.clear();
    assertEquals(3, queryService.countBooks(true));
    long statementsWithFetchJoin = stats.getPrepareStatementCount();
    assertTrue(statementsWithNPlusOne >= 4, "esperava consulta de autores + consultas lazy por autor");
    assertEquals(1, statementsWithFetchJoin, "join fetch deve resolver a fixture em uma consulta");
  }

  @Test void versionColumnRejectsStaleConcurrentUpdate() {
    inventory.saveAndFlush(new InventoryEntity(1L, 10));
    EntityManager first = emf.createEntityManager();
    EntityManager second = emf.createEntityManager();
    try {
      first.getTransaction().begin();
      second.getTransaction().begin();
      InventoryEntity a = first.find(InventoryEntity.class, 1L);
      InventoryEntity b = second.find(InventoryEntity.class, 1L);
      a.setQuantity(11);
      b.setQuantity(12);
      first.getTransaction().commit();
      assertThrows(RollbackException.class, () -> second.getTransaction().commit());
    } finally {
      if (first.getTransaction().isActive()) first.getTransaction().rollback();
      if (second.getTransaction().isActive()) second.getTransaction().rollback();
      first.close(); second.close();
    }
  }
}

class ConcurrencySemanticsTest {
  @Test void controlledInterleavingExposesLostUpdateAndAtomicCounterPreservesInvariant() throws Exception {
    CyclicBarrier barrier = new CyclicBarrier(2);
    class RacyCounter {
      int value;
      void increment() {
        int observed = value;
        try { barrier.await(); } catch (Exception e) { throw new RuntimeException(e); }
        value = observed + 1;
      }
    }
    RacyCounter racy = new RacyCounter();
    Thread t1 = new Thread(racy::increment);
    Thread t2 = new Thread(racy::increment);
    t1.start(); t2.start(); t1.join(); t2.join();
    assertEquals(1, racy.value, "interleaving controlado demonstra lost update");

    AtomicInteger safe = new AtomicInteger();
    Thread a = new Thread(safe::incrementAndGet);
    Thread b = new Thread(safe::incrementAndGet);
    a.start(); b.start(); a.join(); b.join();
    assertEquals(2, safe.get());
  }
}
