<?php

require_once("/var/www/html/entity/FaqRepository.php");

class SearchFaqController
{
    private $faq;

    public function __construct()
    {
        $this->faq = new FaqRepository();
    }

    public function searchFaq(string $searchTerm): array
    {
        return $this->faq->searchFaq($searchTerm);
    }
}