/*

  Copyright © 2013 Simon Forman
  This file is Xerblin.

  Xerblin is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  Xerblin is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with Xerblin.  If not, see <http://www.gnu.org/licenses/>.

*/

var library = {

  self: function self(I) {
    return [[I, I[0]], I[1]];
  },

  jq: function jq(I) {
    I[0][0] = $(I[0][0]);
    return I;
  },

  append: function append(I) {
    var t = xerblin.pop(I[0], 2);
    var result = t[1].append(t[0]);
    return [[result, t[2]], I[1]];
  },

/*
    : function (I) {
      return [I[0], I[1]];
    },
  },
*/

}


//#######################################################################
//  Global namespace.
//#######################################################################

var history_list = [], ns = {};


$(function() {


//#######################################################################
//  Render Stack.
//#######################################################################
function bar() {
  var n = history_list.length;
  var sd = $('#stack_display');
  sd.contents().remove();
  stack_item(history_list[history_list.length - 1], sd);
}

function stack_item(stack, list) {
  if (stack.length == 0) { return; };
  display_item(stack[0], list);
  stack_item(stack[1], list);
}

function display_item(item, list) {
  if (_.isArray(item)) {
    var li = $('<li></li>');
    list.append(li);
    display_array(item, li);
  } else if (_.isString(item)) {
    list.append('<li>&quot;' + item + '&quot;');
  } else if (_.isObject(item) && !_.isUndefined(item.name)) {
    list.append('<li>' + item.name + '()');
  } else {
    list.append('<li>' + item);
  }
}

function display_array(A, list) {
  var d = $('<ul></ul>');
  _.each(A, function(item) { return display_item(item, d); });
  list.append(d);
}


//#######################################################################
//  Interpret commands and update the display.
//#######################################################################

  function post_command(cmd) {
//    console.log('post_command', cmd);
    var I = xerblin.interpret(ns.I, cmd);
//    console.log('post_command', I);
    ns.I = I;
    history_list[0] = I[0];
    bar();
    create_dictionary_buttons(_.keys(xerblin.to_obj(I[1])).sort());
  }
  
  function create_dictionary_buttons(names) {
    $("#dictionary_buttons").find('a').remove();
    _.each(names, function(name) {
      $("#dictionary_buttons").append('<a href="#" id="' + name + '">' + name + '</a>');
    });
    $("#dictionary_buttons").find('a').button().click(function() {
      var cmd = $(this).text();
      post_command([cmd]);
      return false;
    });
  }

//#######################################################################
//  Set up the controls.
//#######################################################################

  $("#meta_controls").buttonset();

  $("form").submit(function() {
    var command = $("#commande").val().split(/\s+/);
    post_command(command);
    $("#commande").val('');
    return false;
  });

  $("#runit").click(function() { return $("form").submit(); });

  $("#stackit").click(function() {
    var cmd = ['"' + $("#commande").val() + '"'];
    post_command(cmd);
    return false;
  });

  $("#clear_entry").button().click(function() {
    $("#commande").val("");
    return false;
  });

//#######################################################################
//  Create Interpreter.
//#######################################################################
  (function() {
    var I = xerblin.create_new_interpreter();
    _.each(library, function(value, key) {
      I[1] = xerblin.insert(I[1], key, value);
    });
    ns.I = I;
    history_list.push(ns.I[0]);
    bar();
    var names = _.keys(xerblin.to_obj(I[1])).sort();
    create_dictionary_buttons(names);
  })();

});

