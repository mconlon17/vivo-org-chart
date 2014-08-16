angular.module('d3DemoApp', ['d3'])
.controller('MainCtrl', ['$scope', function($scope){
    $scope.greeting = "Resize the page to see the re-rendering";
    $scope.data = [
        {"size": "1000", "cx":"50",  "cy":"150", "color":"orange"},
        {"size": "300",  "cx":"200", "cy":"150", "color":"blue"}
    ];
}])
.directive('vennDiagram', ['$window', '$timeout', 'd3Service',
  function($window, $timeout, d3Service) {

  alert("Hello from directive");

    return {
      restrict: 'A',
      scope: {
        data: '='
      },
      link: function(scope, ele, attrs) {
        d3Service.d3().then(function(d3) {

          var renderTimeout;

          var svg = d3.select(ele[0])
            .append('svg')
            .style('width', 300)
            .style('height', 300);

          $window.onresize = function() {
            scope.$apply();
          };

          scope.$watch(function() {
            return angular.element($window)[0].innerWidth;
          }, function() {
            scope.render(scope.data);
          });

          scope.$watch('data', function(newData) {
            scope.render(newData);
          }, true);

          scope.render = function(data) {
            svg.selectAll('*').remove();

            if (!data) return;
            if (renderTimeout) clearTimeout(renderTimeout);

            renderTimeout = $timeout(function() {
              svg.selectAll('circle')
                .data(data)
                .enter()
                .append('circle')
                .attr('cx', function(d) { d.cx ;})
                .attr('cy', function(d) { d.cy ;})
                .attr('r', function(d) { Math.sqrt(d.size/Math.PI); })
                .style("fill", function(d) { d.color; } )
                .style("opacity","0.5");
            }, 200);
          };
        });
      }}
}])