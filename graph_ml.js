var m = [20, 120, 20, 120],
    w = 700 - m[1] - m[3],
    h = 1000 - m[0] - m[2],
    i = 0,
    root,
    descendantPath = [];

var tree = d3.layout.tree()
  .size([w, h]);

var diagonal = d3.svg.diagonal()
  .projection(function(d) { return [d.x, d.y]; });

var vis = d3.select("#tree").append("svg:svg")
  .attr("width", w + m[1] + m[3])
  .attr("height", h + m[0] + m[2])
  .append("svg:g")
  .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

d3.json("server/data.json", function(json) {
  root = json;
  root.x0 = h / 2;
  root.y0 = 0;

  function toggleAll(d, minDepth) {
    if (d.children) {
      d.children.forEach(function(c) {
        toggleAll(c, minDepth - 1)
      });
      if (minDepth <= 0 || minDepth == null)
        toggle(d);
    }
  }

  // Initialize the display to show a few nodes until a certain level.
  toggleAll(root, 3);
  update(root);
});

var scheme = new ColorScheme;
var colors = scheme.from_hue(216)
      .scheme('tetrade')
      .distance(1)
      .colors();

tip = d3.tip().attr('class', 'd3-tip').html(function(d) {
  var s = [];
  if (d.feature) // leafs don't have features
    s.push('Feature: ' + d.feature);
  s.push(d.count + ' samples');
  return s.join('<br>')
});

function update(source) {
  var duration = d3.event && d3.event.altKey ? 5000 : 500;

  // Compute the new tree layout.
  var nodes = tree.nodes(root).reverse();

  // Normalize for fixed-depth.
  nodes.forEach(function(d) { d.y = d.depth * 90; });

  // Update the nodes…
  var node = vis.selectAll("g.node")
    .data(nodes, function(d) { return d.id || (d.id = ++i); });
  vis.call(tip)

  function setNodeProperty(property, value) {
      tree.nodes(root).forEach(function(d) {
        d[property] = value;
      })
  }

  // Enter any new nodes at the parent's previous position.
  var nodeEnter = node.enter().append("svg:g")
    .attr("class", "node")
    .attr("transform", function(d) { return "translate(" + source.x0 + "," + source.y0 + ")"; })
    .on("click", function(d) { toggle(d); update(d); })
    .on("mouseover", function(d) {
      var scope = getScope();
      var path = []
      setNodeProperty('highlight', false)
      var node = d;
      while(node) {
        var decisionPathNode = {
          feature: node.feature,
          threshold: node.threshold,
          side: node.side
        }
        path.unshift(decisionPathNode)
        node.highlight = true;
        node = node.parent;
        scope.transformPath(path)
      }
      update(root)
      scope.$apply();
      tip.show(d)
    })
    .on('mouseout', tip.hide);

  function colorCircle(d) {
    return d.featureIdx != null ? "#" + colors[d.featureIdx] : "gray"
  }

  nodeEnter.append("svg:circle")
    .attr("r", 1e-6)
    .style("fill", function(d) {return d._children ? "lightsteelblue" : colorCircle(d); })
    .style("stroke", colorCircle)

  // Transition nodes to their new position.
  var nodeUpdate = node.transition()
    .duration(duration)
    .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
    .each("end", function(d) {
      
    });

  nodeUpdate.select("circle")
    .attr("r", 10)
    .style("cursor", function(d) { return d.children || d._children ? "pointer" : ""; })
    .style("fill", function(d) {return tinycolor(colorCircle(d)).lighten(3).toString(); })

  // Transition exiting nodes to the parent's new position.
  var nodeExit = node.exit().transition()
    .duration(duration)
    .attr("transform", function(d) { return "translate(" + source.x + "," + source.y + ")"; })
    .remove();

  nodeExit.select("circle")
    .attr("r", 1e-6);

  // Update the links…
  var link = vis.selectAll("path.link")
  .data(tree.links(nodes), function(d) { return d.target.id; });

  // Enter any new links at the parent's previous position.
  link.enter().insert("svg:path", "g")
    .attr("class", "link")
    .attr("d", function(d) {
      var o = {x: source.x0, y: source.y0};
      return diagonal({source: o, target: o});
    })
    .transition()
    .duration(duration)
    .attr("d", diagonal);

  // Transition links to their new position.
  link.transition()
    .style("stroke-width", function(d) {
      if (d.target.highlight) {
        return "10px"
      }
    })
    .duration(duration)
    .attr("d", diagonal);

  // Transition exiting nodes to the parent's new position.
  link.exit().transition()
    .duration(duration)
    .attr("d", function(d) {
      var o = {x: source.x, y: source.y};
      return diagonal({source: o, target: o});
    })
    .remove();

  // Stash the old positions for transition.
  nodes.forEach(function(d) {
    d.x0 = d.x;
    d.y0 = d.y;
  });
}

// Toggle children.
function toggle(d) {
  if (d.children) {
    d._children = d.children;
    d.children = null;
  } else {
    d.children = d._children;
    d._children = null;
  }
}