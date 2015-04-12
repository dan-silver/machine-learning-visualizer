function transformPath(decisionPath) {
	var path = []

	for (var i=1; i<decisionPath.length; i++) {
		path.push({
			feature: decisionPath[i-1].feature,
			side: decisionPath[i].side == 'left' ? "<=" : ">",
			threshold: decisionPath[i-1].threshold.toPrecision(5),
			level: i
		})
	}
	path.push({feature: decisionPath[decisionPath.length-1].feature, level: decisionPath.length})
	return path;
}