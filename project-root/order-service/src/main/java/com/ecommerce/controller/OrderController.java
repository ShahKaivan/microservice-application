// order-service/src/main/java/com/ecommerce/controller/OrderController.java
package main.java.com.ecommerce.controller;

import com.ecommerce.model.Order;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/orders")
public class OrderController {
    private final KafkaTemplate<String, String> kafkaTemplate;

    public OrderController(KafkaTemplate<String, String> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    @PostMapping
    public Order createOrder(@RequestBody Order order) {
        // Save order logic here
        kafkaTemplate.send("order-events", "Order created: " + order.getId());
        return order;
    }

    @GetMapping("/{id}")
    public Order getOrder(@PathVariable Long id) {
        // Get order logic here
        return new Order();
    }
}