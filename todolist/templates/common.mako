<!DOCTYPE html>
<html lang="en" dir="ltr">

<head>
  <meta charset="utf-8">
  <title>To Do List</title>
    <link rel="stylesheet" href="${request.static_url('todolist:static/css/styles.css')}"/>
</head>

<body>
<%include file="header.mako"/>

${next.body()}

<%include file="footer.mako"/>
</body>

</html>