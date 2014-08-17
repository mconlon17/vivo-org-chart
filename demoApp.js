var d3DemoApp = angular.module('d3DemoApp', [])
	.directive('dynCircle', function ($parse) {

	return {
		restrict: 'E',
		scope: {
			val: '=',
		},
		link: function (scope, element, attrs) {

		// set up initial svg object
		
		var viz = d3.select(element[0])
			.append("svg")
			.attr("width", 300)
			.attr("height",300);

		alert("In Link r="+scope.data);

		var circles = viz.selectAll("circle")
			.data(scope.data)
			.enter()
			.append("circle")
				.attr("cx",function(d) {return d.cx;})
				.attr("cy",function(d) {return d.cy;})
				.attr("r",function(d) {return d.r;})
				.style("fill",function(d) {return d.color;});

		scope.$watch('val', function (newVal, oldVal) {
		
		alert("In watch. val was "+oldVal+" now "+newVal+"\nWill transition circle.");
	  
			viz.selectAll("circle").transition()
				.duration(750)
				.delay(200)
				.attr("r", function() { return newVal.r; });
		});
    }
  }
});

d3DemoApp.controller('dynCircleController', function dynCircleController ($scope) {

    $scope.radius = "75";

	$scope.getData = function(){
	    $scope.data = [{"cx":150,"cy":150,"r":$scope.radius,"color":"purple"}];
	};

	$scope.getData();

});