var app = angular.module('ml', []);

function getScope() {
	return angular.element(document.getElementsByTagName('body')).scope()
}

app.controller('tree', function ($scope) {
  $scope.decisionPath = [];
});