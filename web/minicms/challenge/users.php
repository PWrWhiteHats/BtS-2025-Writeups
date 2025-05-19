<!-- users.php -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MiniatureCMS - Users</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
        }
        header {
            background-color: #333;
            color: #fff;
            padding: 1rem 0;
            text-align: center;
        }
        nav {
            background-color: #444;
            padding: 0.5rem;
            text-align: center;
        }
        nav a {
            color: #fff;
            text-decoration: none;
            margin: 0 1rem;
        }
        nav a:hover {
            text-decoration: underline;
        }
        main {
            padding: 2rem;
            max-width: 800px;
            margin: 0 auto;
            background: #fff;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        footer {
            text-align: center;
            padding: 1rem 0;
            background-color: #333;
            color: #fff;
            margin-top: 2rem;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            padding: 0.5rem 0;
            border-bottom: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <header>
        <h1>Welcome to MiniatureCMS</h1>
    </header>
    <nav>
        <a href="/">Home</a>
        <a href="/files">Files</a>
        <a href="/users">Users</a>
        <a href="/about">About</a>
        <a href="/auth/login" style="float: right;">Login</a>
    </nav>
    <main>
        <h2>MiniatureCMS  Users</h2>
        <ul>
            <?php foreach ($users as $user): ?>
                <li><?= htmlspecialchars($user['name']) ?> (<?= htmlspecialchars($user['email']) ?>)</li>
            <?php endforeach; ?>
        </ul>
    </main>
    <footer>
        <p>&copy; 2025 MiniatureCMS. All rights reserved.</p>
    </footer>
</body>
</html>
