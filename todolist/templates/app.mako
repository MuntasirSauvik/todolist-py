<!DOCTYPE html>
<html lang="en" ng-app="todolistApp" ng-strict-di>

<head>
  <meta charset="utf-8">
  <title>To Do List AngularJS</title>
  <!-- Legacy code -->
  <!-- <link rel="stylesheet" href="app.css" />
  <script src="lib/angular/angular.js"></script>
  <script src="lib/angular-route/angular-route.js"></script>
  <script src="app.js"></script>
  <script src="modules/app/app-controller.js"></script>
  <script src="modules/todoList/todo-list-controller.js"></script> -->
  <link rel="stylesheet" href="${request.static_url('todolist:static/css/styles.min.css')}" />
  <script src="${request.static_url('todolist:static/js/vendor.min.js')}"></script>
  <script src="${request.static_url('todolist:static/js/templates.min.js')}"></script>
  <script src="${request.static_url('todolist:static/js/scripts.min.js')}"></script>
</head>

<body ng-controller="AppController">
    <!-- <pre>$location.path() = {{$location.path()}}</pre>
    <pre>$route.current.templateUrl = {{$route.current.templateUrl}}</pre>
    <pre>$route.current.params = {{$route.current.params}}</pre>
    <pre>$route.current.scope.name = {{$route.current.scope.name}}</pre>
    <pre>$routeParams = {{$routeParams}}</pre> -->

    <div ng-view>

    </div>

</body>
<footer>
  Copyright 2020 Muntasir Sauvik
</footer>
</html>
