<?php
// Função atualizada para receber o VALOR (Preço) no terceiro parâmetro
function sendToThingSpeak($writeKey, $productId, $valor) {
    
    // 1. Validação básica
    if (empty($writeKey)) {
        return "Erro: Write Key vazia nas configurações.";
    }
    
    // 2. Montagem da URL
    // Note que agora &field2= recebe a variável $valor
    $url = "https://api.thingspeak.com/update?api_key=" . $writeKey . 
           "&field1=" . $productId . 
           "&field2=" . $valor . 
           "&status=HTTPSENT";

    // 3. Configuração do cURL (O carteiro)
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 15); // Espera no máximo 15s
    
    // Importante para evitar erros de SSL em alguns servidores
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    
    // 4. Envio e Coleta da Resposta
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);

    // 5. Tratamento de Erros
    
    // Se o cURL falhar (sem internet, DNS erro, etc)
    if ($response === false) {
        return "Erro cURL: " . $curlError;
    }

    // O ThingSpeak retorna "0" se você enviar rápido demais (menos de 15s)
    if ($response == '0') {
        return "ThingSpeak bloqueou (Aguarde 15 segundos entre cliques).";
    }

    // Se deu certo, o ThingSpeak retorna um número (ID da entrada, ex: 2845)
    // E o código HTTP deve ser 200 (OK)
    if ($httpCode == 200 && intval($response) > 0) {
        return true; // Sucesso absoluto!
    }

    return "Erro HTTP Code: " . $httpCode . " Resp: " . $response;
}