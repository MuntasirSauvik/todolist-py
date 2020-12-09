'use strict';

var frameworkModules = ['ngRoute'];
var appModules = ['templates'];

var allModules = [].concat(frameworkModules, appModules);
angular.module('todolistApp', allModules);


require('./modules/todoList');
