angular.module('myApp.directives', [d3])
	.directive('dynCircle', function ($parse) {

	var circleData = [{"cx":150,"cy":150,"r":50,"color":"purple"}];
		
	return {
		restrict: 'E',
		scope: {
			r: '=',
		},
		link: function (scope, element, attrs) {

		// set up initial svg object
		
		var viz = d3.select(element[0])
			.append("svg")
			.attr("width", 300)
			.attr("height",300);
				
		var circles = viz.selectAll("circle")
			.data(circleData)
			.enter()
			.append("circle")
				.attr("cx",function(d) {return d.cx;})
				.attr("cy",function(d) {return d.cy;})
				.attr("r",function(d) {return d.r;})
				.style("fill",function(d) {return d.color;});

		scope.$watch('r', function (newVal, oldVal) {
		
		alert("In watch. r was "+oldVal+" now "+newVal+"\nWill transition circle.");
	  
			viz.selectAll("circle").transition()
				.duration(750)
				.delay(200)
				.attr("r", function() { return newVal; });

		});
    }
  }
});

d3DemoApp.controller('dynCircleController', function dynCircleController ($scope) {
	$scope.inputr = "75";
});