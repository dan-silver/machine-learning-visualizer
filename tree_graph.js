var app = angular.module('ml', []);

function getScope() {
  return angular.element(document.getElementsByTagName('body')).scope()
}

app.controller('tree', function ($scope) {
  $scope.decisionPath = [];

  //converts edges to nodes
  $scope.transformPath = function(decisionPath) {
    var path = []

    for (var i=1; i<decisionPath.length; i++) {
      path.push({
        feature: decisionPath[i-1].feature,
        side: decisionPath[i].side == 'left' ? "<=" : ">",
        threshold: decisionPath[i-1].threshold.toPrecision(5)
      })
    }
    path.push({feature: decisionPath[decisionPath.length-1].feature})

    $scope.decisionPath = path;
  }
});