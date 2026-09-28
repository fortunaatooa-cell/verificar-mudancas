package fixture;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.persistence.Version;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.support.TransactionSynchronizationManager;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
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

record CustomerWirePayload(@JsonProperty("customerName") String name) {}
record CreateOrderRequest(@NotBlank String label) {}

@RestController
@RequestMapping("/contracts")
class ContractController {
  @GetMapping("/customer") CustomerWirePayload customer() { return new CustomerWirePayload("Ada"); }
  @PostMapping("/orders") ResponseEntity<Void> create(@Valid @RequestBody CreateOrderRequest request) {
    return ResponseEntity.noContent().build();
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

@Entity
@Table(name = "audit_fixture")
class AuditEntity {
  @Id private Long id;
  private String message;
  protected AuditEntity() {}
  AuditEntity(Long id, String message) { this.id = id; this.message = message; }
}
interface AuditRepository extends JpaRepository<AuditEntity, Long> {}

@Service
class AuditService {
  private final AuditRepository repository;
  AuditService(AuditRepository repository) { this.repository = repository; }
  @Transactional(propagation = Propagation.REQUIRES_NEW)
  void audit(long id) { repository.save(new AuditEntity(id, "committed independently")); }
}

@Service
class OuterTransactionService {
  private final OrderRepository orders;
  private final AuditService audit;
  OuterTransactionService(OrderRepository orders, AuditService audit) { this.orders = orders; this.audit = audit; }
  @Transactional void writeThenFail(long orderId, long auditId) {
    orders.save(new OrderEntity(orderId, "outer"));
    audit.audit(auditId);
    throw new IllegalStateException("outer rollback");
  }
}

@Entity
@Table(name = "authors_fixture")
class AuthorEntity {
  @Id private Long id;
  private String name;
  @OneToMany(mappedBy = "author", fetch = FetchType.LAZY, cascade = CascadeType.ALL)
  private List<BookEntity> books = new ArrayList<>();
  protected AuthorEntity() {}
  AuthorEntity(Long id, String name) { this.id = id; this.name = name; }
  void addBook(BookEntity book) { books.add(book); book.author = this; }
  List<BookEntity> getBooks() { return books; }
}

@Entity
@Table(name = "books_fixture")
class BookEntity {
  @Id private Long id;
  private String title;
  @ManyToOne(fetch = FetchType.LAZY) AuthorEntity author;
  protected BookEntity() {}
  BookEntity(Long id, String title) { this.id = id; this.title = title; }
}

interface AuthorRepository extends JpaRepository<AuthorEntity, Long> {
  @Query("select distinct a from AuthorEntity a left join fetch a.books")
  List<AuthorEntity> findAllWithBooks();
}

@Service
class AuthorQueryService {
  private final AuthorRepository repository;
  AuthorQueryService(AuthorRepository repository) { this.repository = repository; }
  @Transactional(readOnly = true) int countBooks(boolean fetchJoin) {
    List<AuthorEntity> authors = fetchJoin ? repository.findAllWithBooks() : repository.findAll();
    return authors.stream().mapToInt(a -> a.getBooks().size()).sum();
  }
}

@Entity
@Table(name = "inventory_fixture")
class InventoryEntity {
  @Id private Long id;
  private int quantity;
  @Version private long version;
  protected InventoryEntity() {}
  InventoryEntity(Long id, int quantity) { this.id = id; this.quantity = quantity; }
  void setQuantity(int quantity) { this.quantity = quantity; }
}
interface InventoryRepository extends JpaRepository<InventoryEntity, Long> {}
