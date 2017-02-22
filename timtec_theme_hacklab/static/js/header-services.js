(function(angular){
    'use strict';
    var app = angular.module('header.services', ['ngResource']);

    app.factory('UnreadNotification', ['$resource', function($resource){
        return $resource('/base/api/unread-notification/:id',
            {'id' : '@id'},
            {'update': {'method': 'PUT'} });
    }]);

})(window.angular);
