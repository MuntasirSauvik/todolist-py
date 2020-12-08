'use strict'

// Define the `TodoListController` controller on the `todolistApp` module
angular.module('todolistApp').controller('TodoListController', ['$scope', '$http', '$routeParams', '$httpParamSerializerJQLike', function TodoListController($scope, $http, $routeParams, $httpParamSerializerJQLike) {
  var todoList = $routeParams.listName || 'Home'; // fetch this from angular route
  $scope.newItemText = 'hello';

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
    var url = baseUrl + '/api/lists/' + todoList + '/items/' + item.id + '/mark_complete';

    var params = {completed: item.completed ? '1' : '0'};
    var encodedData = $httpParamSerializerJQLike(params);
    $http.post(url, encodedData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    .then(function (response) {
        $scope.listItems(todoList);
    }, function (response) {
      console.log("Error: toggleComplete failed.");
    });
  }

  $scope.addItem = function() {
    console.log('addItem called');
    console.log('item clicked', $scope.newItem);
    var url = baseUrl + '/api/lists/' + todoList + '/items/add';
    var params = {newItem: $scope.newItem};
    var encodedData = $httpParamSerializerJQLike(params);
    $http.post(url, encodedData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    .then(function (response) {
        $scope.listItems(todoList);
    }, function (response) {
      console.log("Error: addItem failed.");
    });
  }

}]);
