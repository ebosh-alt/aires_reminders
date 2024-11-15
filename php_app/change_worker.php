<?php
$url = "http://aires.astoria-tula.ru/sharedapi/worker/update";


$data = json_decode(file_get_contents('php://input'), true);
$apikey = $data["api_key"];  // Первый параметр
$user_id = $data["user_id"];    // Второй параметр
$value_field = $data["value_field"];    // Второй параметр
// $apikey = "21d1c8300ca07c06bf8f3aac3c16c275";  // Первый параметр
// $user_id = "1152";    // Второй параметр
// $value_field = "Лиды Включены";    // Второй параметр
$params = array(
    array(
        'id' => $user_id,
        'fields' => array(
            array('id' => 3657, 'value' => $value_field),
        )
    )
);

$post = array(
    'apikey' => "$apikey",
    'params' => $params
);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($post));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$response = curl_exec($ch);
curl_close($ch);
$result = json_decode($response, true);
echo json_encode($result, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
?>