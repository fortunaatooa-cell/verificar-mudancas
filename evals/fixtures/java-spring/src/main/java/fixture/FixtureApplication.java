package fixture;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.support.TransactionSynchronizationManager;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
public class FixtureApplication {
  public static void main(String[] args) { SpringApplication.run(FixtureApplication.class, args); }
}

@Entity
@Table(name = "orders_fixture")
class OrderEntity {
  @Id private Long id;
  private String label;
  protected OrderEntity() {}
  OrderEntity(Long id, String label) { this.id = id; this.label = label; }
  Long getId() { return id; }
  String getLabel() { return label; }
}

interface OrderRepository extends JpaRepository<OrderEntity, Long> {}
record OrderView(long id, String label) {}

@Service
class OrderService {
  private final OrderRepository repository;
  private final boolean syntheticFallback;
  OrderService(OrderRepository repository, @Value("${fixture.synthetic-fallback:true}") boolean syntheticFallback) {
    this.repository = repository; this.syntheticFallback = syntheticFallback;
  }
  Optional<OrderView> find(long id) {
    Optional<OrderView> found = repository.findById(id).map(order -> new OrderView(order.getId(), order.getLabel()));
    if (found.isPresent() || !syntheticFallback) return found;
    return Optional.of(new OrderView(id, "synthetic"));
  }
}

@RestController
@RequestMapping("/orders")
class OrderController {
  private final OrderService service;
  OrderController(OrderService service) { this.service = service; }
  @GetMapping("/{id}") ResponseEntity<OrderView> get(@PathVariable long id) {
    return service.find(id).map(ResponseEntity::ok).orElseGet(() -> ResponseEntity.notFound().build());
  }
}

@Service
class TransactionScenarioService {
  private final OrderRepository repository;
  TransactionScenarioService(OrderRepository repository) { this.repository = repository; }
  @Transactional void saveFlushThenRuntimeFailure(long id) {
    repository.saveAndFlush(new OrderEntity(id, "runtime"));
    throw new IllegalStateException("runtime failure after flush");
  }
  @Transactional void saveFlushThenCheckedFailure(long id) throws CheckedFixtureException {
    repository.saveAndFlush(new OrderEntity(id, "checked"));
    throw new CheckedFixtureException("checked failure after flush");
  }
  static class CheckedFixtureException extends Exception { CheckedFixtureException(String message) { super(message); } }
}

@Service
class TransactionProbe {
  boolean outerCallsInner() { return innerTransactional(); }
  @Transactional boolean innerTransactional() { return TransactionSynchronizationManager.isActualTransactionActive(); }
}
