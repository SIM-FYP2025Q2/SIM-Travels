<?php

require_once("/var/www/html/entity/FaqRepository.php");

class ViewAllFaqController
{
    private $faq;

    public function __construct()
    {
        $this->faq = new FaqRepository();
    }

    public function readAllFaq(): array
    {
        return $this->faq->readAllFaq();
    }
}