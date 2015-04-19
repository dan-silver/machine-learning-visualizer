function transformPath(decisionPath) {
	var path = []

	for (var i=1; i<decisionPath.length; i++) {
		var node = {
			feature: decisionPath[i-1].feature,
			side: decisionPath[i].side == 'left' ? "<=" : ">",
			threshold: decisionPath[i-1].threshold.toPrecision(5),
			featureIdx: decisionPath[i-1].featureIdx,
			level: i
		}
		//copy all properties of decisionPath[i] to node if they won't overide a property
		for (var attrname in decisionPath[i]) {
			if (node[attrname] == null)
				node[attrname] = decisionPath[i][attrname];
		}
		path.push(node)
	}

	return path;
}

var tip_features = {
  feature: function(d) { return 'Feature: ' + d.feature },
  count: function(d) { return d.count + ' samples' },
  dataPercentage: function(d) { return d.dataPercentage + '% of the data'},
  impurity: function(d) { return 'Impurity: ' + d.impurity}
}