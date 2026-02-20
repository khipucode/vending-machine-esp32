<?php
// Configurações de Banco de Dados
define('DB_HOST', 'localhost');
define('DB_NAME', 'leaote14_vending'); // ALTERE AQUI
define('DB_USER', 'leaote14_admin');    // ALTERE AQUI
define('DB_PASS', 'network21tele');      // ALTERE AQUI


// Configurações de Admin
define('ADMIN_USER', 'admin');
define('ADMIN_PASS', '123456'); // ALTERE PARA UMA SENHA FORTE

// URL Base (ajusta automaticamente, mas pode forçar se necessário)
$protocol = isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http";
define('BASE_URL', $protocol . "://" . $_SERVER['HTTP_HOST']);

// Fuso Horário
date_default_timezone_set('America/Sao_Paulo');