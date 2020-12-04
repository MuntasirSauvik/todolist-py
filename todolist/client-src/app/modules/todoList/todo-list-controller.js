'use strict'

// Define the `TodoListController` controller on the `todolistApp` module
angular.module('todolistApp').controller('TodoListController', function TodoListController($scope, $http, $routeParams) {
  var todoList = $routeParams.listName || 'Home'; // fetch this from angular route

  //`${baseUrl}/api/lists/get/${todoList}`

  $scope.listItems = function(listName) {
    $http.get(baseUrl + '/api/lists/get/' + listName)
    .then(function(response) {
      if(response.data.result) {
        $scope.items = response.data.object;
      } else {
        // error handler of some sort
      }
    });
  };
  $scope.listItems(todoList);

  $scope.toggleComplete = function(item) {
    console.log('item clicked', item);
    item.completed = !item.completed;
    // send update to server
    //$scope.listItems(todoList);
  }

  $scope.addItem = function() {
    // do item adding

    $scope.listItems(todoList);
  }

});
