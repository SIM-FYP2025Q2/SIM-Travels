<?php

use PHPUnit\Framework\TestCase;

require_once '/var/www/html/entity/FaqRepository.php';
require_once '/var/www/html/entity/Database.php';

// PHPUnit Testing for FaqRepository
class FaqRepositoryTest extends TestCase
{
    private $faqRepository;
    private static $categoryId;
    private static $faqId;
    private static $categoryName = 'PHPUnit Test Category';
    private static $faqQuestion = 'PHPUnit Test Question?';
    private static $faqAnswer = 'PHPUnit Test Answer.';
    private static $faqLink = 'https://example.com';

    protected function setUp(): void
    {
        $this->faqRepository = new FaqRepository();

        // 1. Create a test category
        $this->faqRepository->createCategory(self::$categoryName);
        
        // Fetch the created category's ID
        $db_conn = Database::getConnection();
        $stmt = $db_conn->prepare("SELECT id FROM Category WHERE category = :name");
        $stmt->execute(['name' => self::$categoryName]);
        self::$categoryId = $stmt->fetchColumn();

        // 2. Create a test FAQ
        $this->faqRepository->createFaq(self::$faqQuestion, self::$faqAnswer, self::$categoryId, self::$faqLink);

        // Fetch the created FAQ's ID
        $stmt = $db_conn->prepare("SELECT id FROM FAQ WHERE question = :question");
        $stmt->execute(['question' => self::$faqQuestion]);
        self::$faqId = $stmt->fetchColumn();
    }

    // Test 1: Create a new category
    public function testCreateCategory()
    {
        $result = $this->faqRepository->createCategory('Temporary Category');
        $this->assertTrue($result);
        
        // Verify category exists
        $db_conn = Database::getConnection();
        $stmt = $db_conn->prepare("SELECT id FROM Category WHERE category = 'Temporary Category'");
        $stmt->execute();
        $this->assertTrue($stmt->fetchColumn() !== false);
        
        // Clean up
        $stmt = $db_conn->prepare("DELETE FROM Category WHERE category = 'Temporary Category'");
        $stmt->execute();
    }

    // Test 2: Read all FAQ categories
    public function testReadAllFaqCategories()
    {
        $categories = $this->faqRepository->readAllFaqCategories();
        $this->assertIsArray($categories);
        
        $found = false;
        foreach ($categories as $category) {
            if ($category['id'] == self::$categoryId && $category['category'] == self::$categoryName) {
                $found = true;
                break;
            }
        }
        $this->assertTrue($found, "Test category not found in all categories list.");
    }

    // Test 3: Search for a specific category
    public function testSearchCategories()
    {
        $categories = $this->faqRepository->searchCategories(self::$categoryName);
        $this->assertIsArray($categories);
        $this->assertNotEmpty($categories, "Search should find the test category.");
        $this->assertEquals(self::$categoryName, $categories[0]['category']);
    }

    // Test 4: Create a new FAQ
    public function testCreateFaq()
    {
        $result = $this->faqRepository->createFaq('Temp Question', 'Temp Answer', self::$categoryId, null);
        $this->assertTrue($result);

        // Verify FAQ exists
        $db_conn = Database::getConnection();
        $stmt = $db_conn->prepare("SELECT id FROM FAQ WHERE question = 'Temp Question'");
        $stmt->execute();
        $tempFaqId = $stmt->fetchColumn();
        $this->assertTrue($tempFaqId !== false);

        // Clean up
        $this->faqRepository->deleteFaq($tempFaqId);
    }

    // Test 5: Read a specific FAQ
    public function testReadFaq()
    {
        $faq = $this->faqRepository->readFaq(self::$faqId);
        $this->assertInstanceOf(FaqRepository::class, $faq);
        $this->assertEquals(self::$faqQuestion, $faq->getQuestion());
        $this->assertEquals(self::$faqAnswer, $faq->getAnswer());
        $this->assertEquals(self::$faqLink, $faq->getLink());
    }

    // Test 6: Read all FAQs
    public function testReadAllFaq()
    {
        $faqs = $this->faqRepository->readAllFaq();
        $this->assertIsArray($faqs);

        $found = false;
        foreach ($faqs as $faq) {
            if ($faq->getId() == self::$faqId) {
                $found = true;
                break;
            }
        }
        $this->assertTrue($found, "Test FAQ not found in all FAQs list.");
    }

    // Test 7: Update an existing FAQ
    public function testUpdateFaq()
    {
        $newQuestion = "Updated PHPUnit Question?";
        $newAnswer = "Updated PHPUnit Answer.";
        $status = $this->faqRepository->updateFaq(self::$faqId, $newQuestion, $newAnswer, self::$categoryId, null);
        $this->assertTrue($status);

        $updatedFaq = $this->faqRepository->readFaq(self::$faqId);
        $this->assertEquals($newQuestion, $updatedFaq->getQuestion());
        $this->assertEquals($newAnswer, $updatedFaq->getAnswer());
        $this->assertNull($updatedFaq->getLink());
    }

    // Test 8: Search for a specific FAQ
    public function testSearchFaq()
    {
        $faqs = $this->faqRepository->searchFaq("PHPUnit");
        $this->assertIsArray($faqs);
        $this->assertNotEmpty($faqs, "Search should find the updated test FAQ.");
        $this->assertEquals(self::$faqId, $faqs[0]->getId());
    }

    protected function tearDown(): void
    {
        $this->faqRepository->deleteFaq(self::$faqId);
        $this->faqRepository->deleteCategory(self::$categoryId);
    }
}
