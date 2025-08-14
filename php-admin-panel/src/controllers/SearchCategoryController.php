<?php

require_once("/var/www/html/entity/FaqRepository.php");

class SearchCategoryController
{
    private $faqRepository;

    public function __construct()
    {
        $this->faqRepository = new FaqRepository();
    }

    public function searchCategories(string $searchTerm): array
    {
        return $this->faqRepository->searchCategories($searchTerm);
    }
}
