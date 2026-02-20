<?php
function logEvent($pdo, $type, $message) {
    $stmt = $pdo->prepare("INSERT INTO logs (event_type, message) VALUES (?, ?)");
    $stmt->execute([$type, $message]);
}

function getSettings($pdo) {
    $stmt = $pdo->query("SELECT * FROM settings WHERE id = 1");
    return $stmt->fetch();
}