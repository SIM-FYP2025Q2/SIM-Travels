<?php

require_once("Database.php");

class FaqRepository
{
    protected int $id;
    protected string $question;
    protected string $answer;
    protected int $category_id;
    protected ?string $link;
    protected string $category;
    protected int $is_synced;

    /**
     * Creates a new FAQ entry in the database.
     *
     * @param string $question The question to be added.
     * @param string $answer The answer to the question.
     * @param string $category_id The ID of the category to which the FAQ belongs.
     * @param ?string $link Optional link related to the FAQ (nullable).
     *
     * @return bool Returns true if the FAQ was created successfully, false otherwise.
     */
    public function createFaq(string $question, string $answer, string $category_id, ?string $link): bool
    {
        $db_conn = Database::getConnection();
        try {
            // SQL Statement
            $sql = "INSERT INTO `FAQ` (`question`, `answer`, `category_id`)
                    VALUES (:question, :answer, :category_id)";

            // Include 'link' metadata field if provided.
            if (!is_null($link)) {
                $sql = "INSERT INTO `FAQ` (`question`, `answer`, `category_id`, `link`)
                        VALUES (:question, :answer, :category_id, :link)";
            }

            // Bind Paramaters
            $stmt = $db_conn->prepare($sql);
            $stmt->bindParam(':question', $question);
            $stmt->bindParam(':answer', $answer);
            $stmt->bindParam(':category_id', $category_id);

            // Bind `link` if provided
            if (!is_null($link)) {
                $stmt->bindParam(':link', $link);
            }

            // Execute Statement
            $execResult = $stmt->execute();

            // If execution was sucessful, return true
            // Otherwise, return false
            if ($execResult) {
                return true;
            } else {
                return false;
            }
        } catch (PDOException $e) {
            error_log("Database insert failed: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Reads a specific FAQ record by its ID.
     *
     * @param int $id The ID of the FAQ to read.
     *
     * @return FaqRepository An instance of FaqRepository if successful
     */
    public function readFaq(int $id): ?FaqRepository
    {
        $db_conn = Database::getConnection();

        try {
            // SQL Statement
            $sql = "SELECT F.*, C.category
                    FROM FAQ AS F
                    LEFT JOIN Category AS C ON F.category_id = C.id
                    WHERE F.id = :id";

            // Bind Parameters
            $stmt = $db_conn->prepare($sql);
            $stmt->bindParam(':id', $id);
            $execResult = $stmt->execute();

            // If execution was sucessful, return object
            // Otherwise, return null
            if ($execResult) {
                $faq = $stmt->fetchObject('FaqRepository');
                return $faq;
            } else {
                return null;
            }
        } catch (PDOException $e) {
            error_log("Database query failed: " . $e->getMessage());
            return null;
        }
    }

    /**
     * Reads all FAQ records from the database.
     *
     * @return array An array of FaqRepository objects representing all FAQs.
     */
    public function readAllFaq(): array
    {
        $db_conn = Database::getConnection();
        try {
            // SQL Statement
            $sql = "SELECT F.*, C.category
                    FROM FAQ AS F
                    LEFT JOIN Category AS C ON F.category_id = C.id";
            $stmt = $db_conn->prepare($sql);
            $execResult = $stmt->execute();

            // If execution was sucessful, return array of objects
            // Otherwise, return null
            if ($execResult) {
                $faq = $stmt->fetchAll(PDO::FETCH_CLASS, 'FaqRepository');
                return $faq;
            } else {
                return [];
            }
        } catch (PDOException $e) {
            error_log("Database query failed: " . $e->getMessage());
            return [];
        }
    }

    /**
     * Reads all FAQ categories.
     *
     * @return array An array of string representing all FAQs categories.
     */
    public function readAllFaqCategories(): array {
        $db_conn = Database::getConnection();
        try {
            // SQL Statement
            $sql = "SELECT * FROM Category";
            $stmt = $db_conn->prepare($sql);
            $execResult = $stmt->execute();

            // If execution was sucessful, return array of objects
            // Otherwise, return null
            if ($execResult) {
                $categories = $stmt->fetchAll(PDO::FETCH_ASSOC);
                return $categories;
            } else {
                return [];
            }
        } catch (PDOException $e) {
            error_log("Database query failed: " . $e->getMessage());
            return [];
        }
    }

    /**
     * Updates a specific FAQ record by its ID.
     *
     * @param int $id The ID of the FAQ to update.
     * @param string $question The new question for the FAQ.
     * @param string $answer The new answer for the FAQ.
     * @param int $category_id The ID of the category to which the FAQ belongs.
     * @param ?string $link Optional link related to the FAQ (nullable).
     *
     * @return bool Returns true if the FAQ was updated successfully, false otherwise.
     */
    public function updateFaq(int $id, string $question, string $answer, int $category_id, ?string $link): bool
    {
        $db_conn = Database::getConnection();
        try {
            // SQL Statement
            $sql = "UPDATE `FAQ`
                    SET
                        `question` = :question,
                        `answer` = :answer,
                        `category_id` = :category_id,
                        `link` = :link,
                        `is_synced` = 0
                    WHERE `id` = :id";

            // Bind Paramaters
            $stmt = $db_conn->prepare($sql);
            $stmt->bindParam(':question', $question);
            $stmt->bindParam(':answer', $answer);
            $stmt->bindParam(':category_id', $category_id);
            $stmt->bindParam(':id', $id);

            // Bind `link` if provided
            if (!is_null($link)) {
                $stmt->bindParam(':link', $link);
            } else {
                $stmt->bindValue(':link', null, PDO::PARAM_NULL);
            }

            // Execute Statement
            $execResult = $stmt->execute();

            // If execution was sucessful, return true
            // Otherwise, return false
            if ($execResult) {
                return true;
            } else {
                return false;
            }
        } catch (PDOException $e) {
            error_log("Database update failed: " . $e->getMessage());
            return false;
        }
    }

    public function fetchUnsyncedRecords(): array
    {
        $db_conn = Database::getConnection();
        try {
            // SQL Statement
            $sql = "SELECT F.*, C.category
                    FROM FAQ AS F
                    LEFT JOIN Category AS C ON F.category_id = C.id
                    WHERE is_synced = 0";
            $stmt = $db_conn->prepare($sql);
            $execResult = $stmt->execute();

            // If execution was sucessful, return array of objects
            // Otherwise, return null
            if ($execResult) {
                $faq = $stmt->fetchAll(PDO::FETCH_ASSOC);
                return $faq;
            } else {
                return [];
            }
        } catch (PDOException $e) {
            error_log("Database query failed: " . $e->getMessage());
            return [];
        }
    }

    /**
     * Updates a specific FAQ Record's Sync Status
     *
     * @param int $id The ID of the FAQ to update.
     * @param int $status The Sync Status of the FAQ
     *
     * @return bool Returns true if the FAQ was updated successfully, false otherwise.
     */
    public function setSyncStatus(int $id, int $status): bool
    {
        $db_conn = Database::getConnection();
        try {
            // SQL Statement
            $sql = "UPDATE `FAQ`
                    SET `is_synced` = :status
                    WHERE `id` = :id";

            // Bind Paramaters
            $stmt = $db_conn->prepare($sql);
            $stmt->bindParam(':id', $id);
            $stmt->bindParam(':status', $status);

            // Execute Statement
            $execResult = $stmt->execute();

            // If execution was sucessful, return true
            // Otherwise, return false
            if ($execResult) {
                return true;
            } else {
                return false;
            }
        } catch (PDOException $e) {
            error_log("Database update failed: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Deletes a specific FAQ record by its ID.
     *
     * @param int $id The ID of the FAQ to delete.
     *
     * @return bool Returns true if the FAQ was deleted successfully, false otherwise.
     */
    public function deleteFaq(int $id): bool
    {
        $db_conn = Database::getConnection();
        try {
            // Execute SQL Statement
            $stmt = $db_conn->prepare("DELETE FROM `FAQ` WHERE `id` = $id");
            $execResult = $stmt->execute();

            // If execution was sucessful, return true
            // Otherwise, return false
            if ($execResult) {
                return true;
            } else {
                return false;
            }
        } catch (PDOException $e) {
            error_log("Database delete failed: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Searches FAQs based on a search term.
     *
     * @param string $searchTerm The term to search for in questions and categories.
     *
     * @return array An array of FaqRepository objects that match the search criteria.
     */
    public function searchFaq(string $searchTerm): array
    {
        $db_conn = Database::getConnection();
        try {
            // Add Wildcard Operators to Search Term
            $searchTerm = "%" . $searchTerm . "%";

            // SQL Statement
            $sql = "SELECT F.*, C.category
                    FROM FAQ AS F
                    LEFT JOIN Category AS C ON F.category_id = C.id
                    WHERE F.question LIKE :term OR C.category LIKE :term";

            // Bind Parameters
            $stmt = $db_conn->prepare($sql);
            $stmt->bindParam(':term', $searchTerm);

            // Execute Statement
            $execResult = $stmt->execute();

            // If execution was sucessful, return objects
            // Otherwise, return null
            if ($execResult) {
                return $stmt->fetchAll(PDO::FETCH_CLASS, 'FaqRepository');
            } else {
                return [];
            }
        } catch (PDOException $e) {
            error_log("Database search failed: " . $e->getMessage());
            return [];
        }
    }

    // Accessor Methods
    public function getId(): int
    {
        return $this->id;
    }
    public function getQuestion(): string
    {
        return $this->question;
    }
    public function getAnswer(): string
    {
        return $this->answer;
    }
    public function getCategoryId(): int
    {
        return $this->category_id;
    }
    public function getLink(): ?string
    {
        return $this->link;
    }
    public function getCategory(): string
    {
        return $this->category;
    }
    public function is_synced(): bool
    {
        return $this->is_synced == 1 ? true : false;
    }
}