<?php

// Sample PHP file for a Bike Module

/**
 * Class Bike
 * Represents a bicycle with various attributes and functionality.
 */
class Bike {
    
    private $brand;
    private $model;
    private $price;
    private $type;
    
    /**
     * Constructor to initialize the bike attributes.
     * 
     * @param string $brand - The brand of the bike.
     * @param string $model - The model of the bike.
     * @param float $price - The price of the bike.
     * @param string $type - The type of bike (e.g., road, mountain, hybrid).
     */
    public function __construct($brand, $model, $price, $type) {
        $this->brand = $brand;
        $this->model = $model;
        $this->price = $price;
        $this->type = $type;
    }
    
    /**
     * Get the description of the bike.
     * 
     * @return string - Returns a description of the bike.
     */
    public function getDescription() {
        return "This is a {$this->brand} {$this->model}, which is a {$this->type} bike priced at \${$this->price}.";
    }

    /**
     * Apply a discount to the price of the bike.
     * 
     * @param float $discountPercentage - The percentage of the discount.
     * @return float - Returns the discounted price.
     */
    public function applyDiscount($discountPercentage) {
        $discountAmount = ($this->price * $discountPercentage) / 100;
        $this->price -= $discountAmount;
        return $this->price;
    }
    
    /**
     * Print the current price of the bike.
     * 
     * @return void
     */
    public function printPrice() {
        echo "The current price of the bike is \${$this->price}.";
    }
}

?>

