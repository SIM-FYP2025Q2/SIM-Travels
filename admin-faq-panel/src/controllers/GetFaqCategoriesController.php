<?php

require_once("/var/www/html/entity/FaqRepository.php");

class GetFaqCategoriesController
{
    private $faq;

    public function __construct()
    {
        $this->faq = new FaqRepository();
    }

    public function readAllFaqCategories(): array
    {
        return $this->faq->readAllFaqCategories();
    }
}