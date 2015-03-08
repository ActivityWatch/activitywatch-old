app = angular.module('activitywatch', ["ngResource", "ngRoute"]);


app.config(function($routeProvider, $locationProvider) {
    $routeProvider.when("/", {
        templateUrl: "templates/dashboard.html",
        controller: "HomeCtrl"
    });

    $routeProvider.when("/agents/:id", {
        templateUrl: "templates/agent.html",
        controller: "AgentCtrl"
    });

    $routeProvider.when("/agents", {
        templateUrl: "templates/agents.html",
        controller: "AgentsCtrl"
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

function capitalize(s) {
    return s.substr(0, 1).toUpperCase() + s.substr(1);
}

app.controller("BreadcrumbCtrl", function($scope, $location) {
    var generate_pathtree = function() {
        console.log($location.path());
        var dirs = $location.path() == "/" ? [] : $location.path().substr(1).split("/");
        console.log(dirs);
        return _.map(dirs, function(dirname, i, ctx) {
            var link = i == 0 ? "" : _.reduce(ctx.splice(0, i), function(a, b) { return a+"/"+b }) + "/";
            return {
                "name": capitalize(dirname),
                "link": "/" + link + dirname
            }
        });
    };
    $scope.pathtree = generate_pathtree();

    $scope.$on("$routeChangeSuccess", function() {
        $scope.pathtree = generate_pathtree();
        console.log($scope.pathtree);
    });
});

app.controller("AgentListCtrl", function($scope, $resource, $interval) {
    var Agents = $resource("/api/0/agents");
    $scope.refreshing = false;

    var clear_agents = function () {
        $scope.agents = {"watcher": [], "filter": [], "logger": []};
    }

    $scope.update_agents = function() {
        $scope.refreshing = true;
        clear_agents();
        Agents.query({}, function(agents) {
            _.each($scope.agents, function(object, type) {
                $scope.agents[type] = _.filter(agents, function(a) { return a.type == type; })
            });
        })
            .$promise.finally(function() {
                $scope.refreshing = false;
            });
    };
    $scope.update_agents();

    // Updates status of agents every 60 seconds
    $interval(function() {
        $scope.update_agents()
    }, 60*1000);
});

app.controller("AgentCtrl", function($scope, $resource, $routeParams) {
    var Agents = $resource("/api/0/agents/" + $routeParams.id);

    Agents.get({"id": $routeParams.id}, function(agent) {
        console.log(agent);
        $scope.agent = agent;
    });
});

app.controller("AgentsCtrl", function($scope, $resource, $routeParams) {
});
