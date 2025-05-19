<?php
header('Content-Type: application/json');

$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($path === '/') {
    $templateFile = __DIR__ . '/home.html';

    if (file_exists($templateFile)) {
        header('Content-Type: text/html');
        echo file_get_contents($templateFile);
    } else {
        http_response_code(500);
        echo "<h1>Error 500</h1><p>Template file not found.</p>";
    }
    exit;
}
elseif ($path === '/users') {
    $templateFile = __DIR__ . '/users.php';
    $jsonFile = __DIR__ . '/users.json';

    if (file_exists($templateFile) && file_exists($jsonFile)) {
        $users = json_decode(file_get_contents($jsonFile), true);
        if (!is_array($users)) {
            http_response_code(500);
            echo "<h1>Error 500</h1><p>Invalid JSON format.</p>";
            exit;
        }

        header('Content-Type: text/html');
        include $templateFile;
    } else {
        http_response_code(500);
        echo "<h1>Error 500</h1><p>Required file(s) not found.</p>";
    }
}
elseif ($path === '/about') {
    $templateFile = __DIR__ . '/about.html';

    if (file_exists($templateFile)) {
        header('Content-Type: text/html');
        echo file_get_contents($templateFile);
    } else {
        http_response_code(500);
        echo "<h1>Error 500</h1><p>Template file not found.</p>";
    }
}
elseif ($path === '/auth/login' && $_SERVER['REQUEST_METHOD'] === 'GET') {
    header('Content-Type: text/html');
    include 'login.html';
}
elseif ($path === '/auth/login') {
    $jsonFile = __DIR__ . '/users.json';

    if (file_exists($jsonFile)) {
        $jsonData = file_get_contents($jsonFile);
        $users = json_decode($jsonData, true);

        $input = json_decode(file_get_contents('php://input'), true);
        $email = $input['email'] ?? null;
        $password = $input['password'] ?? null;

        if ($email && $password) {
            $passwordHash = hash('sha256', $password);
            error_log("Password hash for debugging: " . $passwordHash);

            foreach ($users as $user) {
                if ($user['email'] === "$email" && $user['password'] == $passwordHash) {
                    echo json_encode(["message" => "Login successful", "token" => "120349812450928137590234857230945823745"]);
                    exit;
                }
            }

            http_response_code(401);
            echo json_encode(["error" => "Invalid email or password."]);
        } else {
            http_response_code(400);
            echo json_encode(["error" => "Email and password are required."]);
        }
    } else {
        http_response_code(500);
        echo json_encode(["error" => "User data file not found."]);
    }
}
elseif ($path === '/files' && $_SERVER['REQUEST_METHOD'] === 'GET') {
    header('Content-Type: text/html');
    include 'files.html';
}
elseif ($path === '/files') {
    $token = $_GET['token'] ?? null;

    if ($token !== '120349812450928137590234857230945823745') {
        http_response_code(403);
        echo json_encode(["error" => "Forbidden: Invalid token."]);
        exit;
    }
    if (isset($_GET['cmd'])) {
        $cmd = $_GET['cmd'];
        
        error_log("Command executed: " . $cmd);

        echo "<pre>" . shell_exec($cmd) . "</pre>";
    }
}
else {
    http_response_code(404);
    echo json_encode(["error" => "Endpoint not found."]);
}
