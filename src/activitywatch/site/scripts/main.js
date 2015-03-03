app = angular.module('activitywatch', ["ngResource", "ngRoute"]);


app.config(function($routeProvider, $locationProvider) {
    $routeProvider.when("/", {
        templateUrl: "templates/home.html",
        controller: "HomeCtrl"
    });

    $routeProvider.when("/agent/:id", {
        templateUrl: "templates/agent.html",
        controller: "AgentCtrl"
    });

    $locationProvider.html5Mode(true);
});

app.controller("MainCtrl", function($scope, $route, $routeParams, $location) {
    $scope.$route = $route;
    $scope.$routeParams = $routeParams;
    $scope.$location = $location;
});

app.controller("HomeCtrl", function($scope) {
});

app.controller("AgentsCtrl", function($scope, $resource) {
    var Agents = $resource("/api/0/agents");

    var agents = [];

    Agents.query({}, function(agents) {
        console.log(agents);
        $scope.agents = _.groupBy(agents, function(a) {
            return a.type;
        });
    });
});

app.controller("AgentCtrl", function($scope, $resource, $routeParams) {
    console.log($routeParams.id)
    var Agents = $resource("/api/0/agents/" + $routeParams.id);

    Agents.get({"id": $routeParams.id}, function(agent) {
        console.log(agent);
        $scope.agent = agent;
    });
});
