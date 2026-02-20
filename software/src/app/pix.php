<?php
class PixPayload {
    /**
     * Gera o payload do Pix (Copia e Cola)
     * @param string $pixKey Chave Pix
     * @param string $name Nome do Recebedor (Max 25 chars)
     * @param string $city Cidade do Recebedor (Max 15 chars)
     * @param float $amount Valor do Pix (ex: 10.50)
     * @param string $txid Identificador da Transação (Opcional, padrão ***)
     * @return string O código Pix Copia e Cola completo
     */
    public static function generate($pixKey, $name, $city, $amount, $txid = '***') {
        // 1. Limpeza e Formatação
        $name = self::cleanString(substr($name, 0, 25)); // Remove acentos
        $city = self::cleanString(substr($city, 0, 15)); // Remove acentos
        $amount = number_format((float)$amount, 2, '.', ''); // Força 0.00
        $txid = preg_replace('/[^a-zA-Z0-9]/', '', $txid); // Apenas alfanumérico
        if (empty($txid)) $txid = '***';

        // 2. Montagem do Payload (TLV: Tag-Length-Value)
        $payload = 
            self::mountValue('00', '01') .                           // Payload Format Indicator
            self::mountValue('26',                                   // Merchant Account Information
                self::mountValue('00', 'br.gov.bcb.pix') . 
                self::mountValue('01', $pixKey)
            ) .
            self::mountValue('52', '0000') .                         // Merchant Category Code
            self::mountValue('53', '986') .                          // Transaction Currency (BRL)
            self::mountValue('54', $amount) .                        // Transaction Amount
            self::mountValue('58', 'BR') .                           // Country Code
            self::mountValue('59', $name) .                          // Merchant Name
            self::mountValue('60', $city) .                          // Merchant City
            self::mountValue('62',                                   // Additional Data Field Template
                self::mountValue('05', $txid)
            ) .
            '6304';                                                  // CRC16 ID

        // 3. Calcula e Adiciona o CRC16
        $payload .= self::getCRC16($payload);

        return $payload;
    }

    // Monta o campo ID + Tamanho + Valor
    private static function mountValue($id, $value) {
        $size = str_pad(strlen($value), 2, '0', STR_PAD_LEFT);
        return $id . $size . $value;
    }

    // Remove acentos e caracteres especiais (Obrigatório para compatibilidade total)
    private static function cleanString($string) {
        $string = preg_replace(array("/(á|à|ã|â|ä)/","/(Á|À|Ã|Â|Ä)/","/(é|è|ê|ë)/","/(É|È|Ê|Ë)/","/(í|ì|î|ï)/","/(Í|Ì|Î|Ï)/","/(ó|ò|õ|ô|ö)/","/(Ó|Ò|Õ|Ô|Ö)/","/(ú|ù|û|ü)/","/(Ú|Ù|Û|Ü)/","/(ñ)/","/(Ñ)/"),explode(" ","a A e E i I o O u U n N"),$string);
        // Remove tudo que não for letra, número ou espaço
        $string = preg_replace('/[^a-zA-Z0-9 ]/', '', $string);
        return strtoupper(trim($string));
    }

    // Algoritmo CRC16 (CCITT-FALSE) - Padrão do Banco Central
    private static function getCRC16($payload) {
        $payload .= "";
        $polinomio = 0x1021;
        $resultado = 0xFFFF;

        if (($length = strlen($payload)) > 0) {
            for ($offset = 0; $offset < $length; $offset++) {
                $resultado ^= (ord($payload[$offset]) << 8);
                for ($bitwise = 0; $bitwise < 8; $bitwise++) {
                    if (($resultado <<= 1) & 0x10000) $resultado ^= $polinomio;
                    $resultado &= 0xFFFF;
                }
            }
        }
        return strtoupper(str_pad(dechex($resultado), 4, '0', STR_PAD_LEFT));
    }
}
?>