// order-service/src/main/java/com/ecommerce/model/OrderItem.java
package com.ecommerce.model;  // Changed from main.java.com.ecommerce.model

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "order_items")
public class OrderItem {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String productId;
    private Integer quantity;
    private Double price;
}