<?

    $pdo = new PDO("mysql:host=localhost;dbname=u171615_db", 'u171615_db', 'DN2005.03.27');
    $stmt = $pdo->prepare('INSERT INTO orders(name, phone, email, cause) VALUES(:name, :phone, :email, :cause)');

    $stmt->bindValue(':name', $_POST['name']);
    $stmt->bindValue(':phone', $_POST['phone']);
    $stmt->bindValue(':email', $_POST['email']);
    $stmt->bindValue(':cause', $_POST['cause']);

    if ($stmt->execute()) {
        echo '1';
    }

?>