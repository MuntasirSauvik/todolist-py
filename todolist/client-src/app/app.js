'use strict';

// Define the `todolistApp` module
var todolistApp = angular.module('todolistApp', []);

var baseUrl = 'http://localhost:6543';

// Define the `TodoListController` controller on the `todolistApp` module
todolistApp.controller('TodoListController', function TodoListController($scope, $http) {
  var todoList = 'Home'; // fetch this from angular route
  //`${baseUrl}/api/lists/get/${todoList}`

  $scope.listItems = function(listName) {
    $http.get(baseUrl + '/api/lists/get/' + listName)
    .then(function(response) {
      if(response.data.result) {
        $scope.listItems = response.data.object;
      } else {
        // error handler of some sort
      }
    });
  };
  $scope.listItems(todoList);



  $scope.addItem = function() {
    // do item adding

    $scope.listItems(todoList);
  }

});
