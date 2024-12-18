<?

    $pdo = new PDO("mysql:host=localhost;dbname=u171615_db", 'u171615_db', 'DN2005.03.27');
    $stmt = $pdo->query('SELECT * FROM orders ORDER BY id DESC');

?>

<table>
<tr>
    <th>ID</th>
    <th>Имя</th>
    <th>Телефон</th>
    <th>E-mail</th>
    <th>Причина обращения</th>
</tr>
    <?
        foreach ($stmt as $row) {
            echo '<tr>';
            echo '<td>' . $row['id'] . '</td>';
            echo '<td>' . $row['name'] . '</td>';
            echo '<td>' . $row['phone'] . '</td>';
            echo '<td>' . $row['email'] . '</td>';
            echo '<td>' . $row['cause'] . '</td>';
            echo '</tr>';
        }
    ?>
</table>