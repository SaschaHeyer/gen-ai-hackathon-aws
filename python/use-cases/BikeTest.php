<?php

use PHPUnit\Framework\TestCase;

class BikeTest extends TestCase
{
    private $bike;

    protected function setUp(): void
    {
        $this->bike = new Bike('Trek', 'Domane', 2000, 'road');
    }

    public function testGetDescription()
    {
        $expectedDescription = "This is a Trek Domane, which is a road bike priced at $2000.";
        $this->assertEquals($expectedDescription, $this->bike->getDescription());
    }

    public function testApplyDiscount()
    {
        $discountedPrice = $this->bike->applyDiscount(10);
        $this->assertEquals(1800, $discountedPrice);
    }

    public function testPrintPrice()
    {
        $this->expectOutputString("The current price of the bike is $2000.");
        $this->bike->printPrice();
    }

    public function testMultipleDiscounts()
    {
        $this->bike->applyDiscount(10);
        $discountedPrice = $this->bike->applyDiscount(5);
        $this->assertEquals(1710, $discountedPrice);
    }
}
