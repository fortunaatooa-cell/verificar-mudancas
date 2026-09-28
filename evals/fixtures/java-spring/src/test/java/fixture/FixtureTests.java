package fixture;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
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
class SpringTransactionSemanticsTest {
  @Autowired OrderRepository repository;
  @Autowired TransactionScenarioService scenarios;
  @Autowired TransactionProbe probe;
  @BeforeEach void clean() { repository.deleteAll(); }
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
}
