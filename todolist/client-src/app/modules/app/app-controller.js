angular.module('todolistApp').config(['$routeProvider', function($routeProvider) {
  $routeProvider
    .when('/:listName', {
      templateUrl: 'modules/todoList/todo-list.html',
      controller: 'TodoListController'
    })
    .otherwise('/Home')
}])

.controller('AppController', [ '$scope', '$route', '$routeParams', '$location', function($scope, $route, $routeParams, $location) {
    $scope.$route = $route;
    $scope.$location = $location;
    $scope.$routeParams = $routeParams;
}]);

var baseUrl = 'http://localhost:6543';
