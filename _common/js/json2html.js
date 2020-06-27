/**
 * The simplest "JSON->HTML" templater with multilanguage support
 * Author: Leonid Arefev
 * Started: 11-05-2013
 * GitHub: https://github.com/wtf-develop/JSONtemplate
 * Web: https://wtf-dev.ru/
 */

// Wrap all widget code into anonymous function expression to avoid conflicts
// that may occur with another code on the page (module pattern).

if ((J2H === undefined) || (Json2Html === undefined)) {
    var J2H = (function($) {
        "use strict";
        var DEBUG = false;
        var translate_prefix = '@str.';

        // Recommended to keep current values of j_var, j_loop and j_templ.
        // But if you want, you can change it. Then test everything again.
        // 2 simbols for open tag and 2 simbols for closing tag.
        var j_var = ['[*', '*]']; // 2 simbols for each not more, not less
        var j_loop = ['[!', '!]']; // 2 simbols for each not more, not less
        var j_templ = ['{{', '}}']; // 2 simbols for each not more, not less


        /**
        // [!template,array,if=`(expression)`!] - content filter
        // example like JavaScript boolen expression.
        // [!template_name,"jsonArray",if=`((in_array(test.arr;;"777"))&&(test.data=="555")||(test.data>>"444"))&&(test.subj!="fff")`!]
        // can use: == , != ,() , || , &&, in_array
        // more: >>
        // less: <<
        */

        /**
         // Recommended server error response format
         // {"error":{"state":true,"title":"ErrorTitle","message":"ErrorMessage","code":intErrorCode}}
         */

        function in_array(arr, value) {
            //return arr.includes(value)
            for (var key in arr) {
                if (arr[key] == value) {
                    return true;
                };
            }
            return false;
        }




        var error_parcer = '';

        function get_from_data(temp_data, name_var) {
            if (name_var === undefined) {
                if (DEBUG) {
                    alert('Json2Html: CRITICAL error. Varialble name is undefined. Check your loop templates')
                }
                console.log('Json2Html: CRITICAL error. Varialble name is undefined. Check your loop templates');
                return '';
            }
            var i = 0;
            var name_vars = name_var.split('.');
            for (i = 0; i < name_vars.length; i++) {
                name_vars[i] = removeSq(my_trim(name_vars[i]));
                if (name_vars[i] == 'this') {
                    continue;
                };
                if (name_vars[i] == 'vardump') {
                    return printObject(temp_data);
                };
                if ((name_vars[i] == 'length') && (Array.isArray(temp_data))) {
                    return temp_data.length;
                }
                if (name_vars[i] == 'random') {
                    return Math.floor((Math.random() * 100000) + 1);
                }

                if (temp_data !== undefined && temp_data !== null && temp_data[name_vars[i]] !== undefined) {
                    temp_data = temp_data[name_vars[i]];
                } else {
                    if (DEBUG) {
                        if (error_parcer.indexOf(name_vars[i]) == -1) {
                            error_parcer = error_parcer + name_vars[i] + ' in (' + name_var + ')\n';
                        };
                    };
                    temp_data = '';
                    break;
                }
            }
            if (temp_data === undefined || temp_data === null) {
                temp_data = '';
            }

            return temp_data;
        }

        function removeSq(s) {
            if (s === null) return '';
            if (typeof s != 'string') return s;
            if (s.length < 3) return s;
            if (s.charAt(0) == '"' && s.charAt(s.length - 1) == '"') {
                s = s.substr(1, s.length - 2);
            }
            if (s.charAt(0) == "'" && s.charAt(s.length - 1) == "'") {
                s = s.substr(1, s.length - 2);
            }
            if (s.charAt(0) == "`" && s.charAt(s.length - 1) == "`") {
                s = s.substr(1, s.length - 2);
            }
            return s;
        }


        function bit_test(num, bit) {
            return ((num >> bit) % 2 != 0)
        }

        var level_parce = 0; //stack overflow protection
        //function change HTML code with templates to HTML code with data.
        function process(name, data) {
            //check stack overflow
            ///********************** loop part ***************************
            var global_filter = '';
            var templates = shadow_templates_object;

            function set_filter(f) {
                global_filter = f;
                global_filter = str_replace('if=`', '', global_filter);
                global_filter = str_replace('`', '', global_filter);
                global_filter = my_trim(global_filter);
                if (global_filter == '') {
                    return false;
                };
                var temp = global_filter;
                temp = str_replace('&&', '~~', temp);
                temp = str_replace('||', '~~', temp);
                temp = str_replace(';;', '~~', temp);
                temp = str_replace('==', '~~', temp);
                temp = str_replace('!=', '~~', temp);
                temp = str_replace('in_array', '~~', temp);
                temp = str_replace('<<', '~~', temp);
                temp = str_replace('>>', '~~', temp);
                temp = str_replace('(', '~~', temp);
                temp = str_replace(')', '~~', temp);
                while (temp.indexOf('~~~') != -1) {
                    temp = str_replace('~~~', '~~', temp);
                }
                temp = temp.split('~~');
                var c = temp.length;
                var i = 0;
                var str = '';
                var tt = true;
                var start = 0;
                for (i = 0; i < c; i++) {
                    temp[i] = my_trim(temp[i]);
                    if (temp[i] == '') {
                        continue;
                    };
                    if (tt) {
                        str = 'data["' + str_replace('.', '"]["', temp[i]) + '"]';
                        global_filter = str_replace_first(temp[i], str, global_filter, start);
                        start = global_filter.indexOf(str, start) + str.length - 2;
                    }; //if tt
                    tt = !tt;
                }; //for
                global_filter = str_replace('>>', '>', global_filter);
                global_filter = str_replace('<<', '<', global_filter);
                global_filter = str_replace(';;', ',', global_filter);
                return false;
            }

            function check_filter(data) {
                if (global_filter == '') {
                    return true;
                };
                var ret = false;
                try {
                    ret = eval('(' + global_filter + ')');
                } catch (e) {
                    debug_log('debug error in filter!' + "\n" + global_filter + "\n" + e.name);
                    ret = false;
                };

                return ret;
            }
            //*********************** loop end ****************************




            name = removeSq(name)
            var limits = -1;
            var defaults = '';
            var page = 0;
            var variable = '';
            if (DEBUG && (level_parce == 0)) {
                error_parcer = '';
            }
            if (level_parce > 15) {
                debug_log('stack overflow in parser detect');
                return '';
            }
            if (templates[name] === undefined) {
                debug_log('template ' + name + ' is UNDEFINED');
                return '';
            };
            level_parce++;
            var str = templates[name];
            var ind_s = 0;
            var ind_e = 0;
            var name_template, crop, then_v, else_v, name_var, name_var2, name_vars, temp, i, temp_template, temp_str, temp_data;
            crop = -1;
            var replace = -1;
            var replaceFrom = '';
            var replaceTo = '';
            var hash = -1;
            var if_type = -1;

            ///parse JSON data variables
            ///parse JSON data variables
            ///parse JSON data variables
            ind_s = 0;
            ind_e = 0;

            while (str.indexOf(j_var[0], ind_s) != -1) {
                ind_s = str.indexOf(j_var[0], ind_s);
                ind_e = str.indexOf(j_var[1], ind_s + j_var[0].length);
                crop = -1;
                replace = -1;
                hash = -1;
                replaceFrom = '';
                replaceTo = '';
                if_type = -1;
                then_v = '';
                else_v = '';
                variable = '';
                if ((ind_e != -1) && ((ind_e - ind_s) < 155) && ((ind_e - ind_s) > 0)) {
                    name_var = str.substr(ind_s + j_var[0].length, ind_e - (ind_s + j_var[0].length));
                    name_var2 = name_var;
                    variable = '';
                    if (name_var.indexOf(',') != -1) {
                        variable = name_var.split(',');
                        name_var2 = variable[0];
                        if ((variable[1] !== undefined) && (variable[1].indexOf('hash32') == 0)) {
                            hash = 1;
                            variable = '';
                        } else if ((variable[1] !== undefined) && (variable[1].indexOf('replace=') != -1)) {
                            if (variable[1].indexOf('`with`') != -1) {
                                variable[1] = variable[1].split('`with`');
                                replaceFrom = variable[1][0];
                                replaceTo = variable[1][1];
                                replaceFrom = str_replace('replace=', '', replaceFrom);
                                replaceFrom = str_replace('`', '', replaceFrom);
                                replaceTo = str_replace('replace=', '', replaceTo);
                                replaceTo = str_replace('`', '', replaceTo);
                                if (replaceFrom.length > 0) {
                                    replace = replaceFrom.length;
                                } else {
                                    replace = -1;
                                }
                            }
                            variable = '';
                        } else if ((variable[1] !== undefined) && (variable[1].indexOf('crop=') != -1)) {
                            crop = parseInt(removeSq(str_replace('crop=', '', variable[1])));
                            if (crop < 1) crop = -1;
                            variable = '';
                        } else if ((variable[1] !== undefined) && (variable[1].indexOf('ift=`') != -1)) {
                            if_type = 1;
                            then_v = '';
                            else_v = '';

                            if (variable[1].indexOf('`then`') != -1) {
                                variable[1] = variable[1].split('`then`');
                                then_v = variable[1][1];
                                else_v = then_v.split('`else`');
                            } else {
                                then_n = undefined
                                else_v = variable[1].split('`else`');
                            }
                            if (else_v[1] === undefined) {
                                else_v = undefined;
                            } else {
                                then_v = else_v[0];
                                else_v = else_v[1];
                            }
                            variable[1] = str_replace('ift=', '', variable[1][0]);
                            variable[1] = my_trim(str_replace('`', '', variable[1]));
                            if (else_v !== undefined) else_v = my_trim(str_replace('`', '', else_v));
                            if (then_v !== undefined) then_v = my_trim(str_replace('`', '', then_v));
                        } else if ((variable[1] !== undefined) && ((variable[1].indexOf('ifc=`') != -1) || (variable[1].indexOf('if=`') != -1))) {
                            if_type = 2;
                            then_v = '';
                            else_v = '';
                            if (variable[1].indexOf('`then`') != -1) {
                                variable[1] = variable[1].split('`then`');
                                then_v = variable[1][1];
                                else_v = then_v.split('`else`');
                            } else {
                                then_n = undefined
                                else_v = variable[1].split('`else`');
                            }


                            if (else_v[1] === undefined) {
                                else_v = undefined;
                            } else {
                                then_v = else_v[0];
                                else_v = else_v[1];
                            }
                            if (variable[1][0].includes('ifc=')) {
                                variable[1] = str_replace('ifc=', '', variable[1][0]);
                            } else {
                                variable[1] = str_replace('if=', '', variable[1][0]);
                            }
                            variable[1] = my_trim(str_replace('`', '', variable[1]));
                            if (else_v !== undefined) else_v = my_trim(str_replace('`', '', else_v));
                            if (then_v !== undefined) then_v = my_trim(str_replace('`', '', then_v));
                        } else if ((variable[1] !== undefined) && (variable[1].indexOf('ifb=`') != -1)) {
                            if_type = 3;
                            then_v = '';
                            else_v = '';
                            if (variable[1].indexOf('`then`') != -1) {
                                variable[1] = variable[1].split('`then`');
                                then_v = variable[1][1];
                                else_v = then_v.split('`else`');
                            } else {
                                then_n = undefined
                                else_v = variable[1].split('`else`');
                            }


                            if (else_v[1] === undefined) {
                                else_v = undefined;
                            } else {
                                then_v = else_v[0];
                                else_v = else_v[1];
                            }
                            variable[1] = str_replace('ifb=', '', variable[1][0]);
                            variable[1] = my_trim(str_replace('`', '', variable[1]));
                            if (else_v !== undefined) else_v = my_trim(str_replace('`', '', else_v));
                            if (then_v !== undefined) then_v = my_trim(str_replace('`', '', then_v));
                        } else {
                            variable = '';
                        }
                    }
                    temp = get_from_data(data, name_var2);
                    if (hash > 0) {
                        temp = murmurhash3_32_gc(temp);
                    } else if (replace > 0) {
                        temp = str_replace(replaceFrom, replaceTo, temp);
                    } else if (crop > 0) {
                        if (temp.length > crop) temp = temp.substr(0, crop) + "...";
                    } else if ((if_type == 1 || if_type == 2) && variable[1] !== undefined) {
                        var checkWithThis = variable[1].toString().toUpperCase();
                        var eqWithThis = false;
                        if (checkWithThis.indexOf('||') != -1) {

                            var checkArr = checkWithThis.split('||');
                            var checkFor = 0;
                            for (checkFor = 0; checkFor < checkArr.length; checkFor++) {
                                if (eqWithThis) continue;
                                eqWithThis = temp.toString().toUpperCase() == (checkArr[checkFor]);
                                if (eqWithThis) {
                                    break;
                                }
                            }
                        } else {
                            eqWithThis = temp.toString().toUpperCase() == checkWithThis;
                        }
                        if (eqWithThis) {
                            if (then_v !== undefined && then_v != '') {
                                if (if_type == 1) {
                                    temp = process(then_v, data);
                                } else {
                                    temp = my_trim(removeSq(then_v));
                                }
                            } else {
                                if (then_v !== undefined) temp = '';
                            };
                        } else {
                            if (else_v !== undefined && else_v != '') {
                                if (if_type == 1) {
                                    temp = process(else_v, data);
                                } else {
                                    temp = my_trim(removeSq(else_v));
                                }
                            } else {
                                if (else_v !== undefined) temp = '';
                            };
                        }
                    } else if ((if_type == 3) && variable[1] !== undefined) { // check bits
                        var checkWithThis = variable[1].toString();
                        var checkFor = 0;
                        var eqWithThis = true;
                        var testbit = parseInt(temp);
                        if (isNaN(testbit)) {
                            eqWithThis = false;
                        } else {
                            for (checkFor = 0; checkFor < checkWithThis.length; checkFor++) {
                                if (!eqWithThis) continue;
                                var ch = checkWithThis.charAt(checkFor);
                                if (ch != '1' && ch != '0') continue;
                                if (bit_test(testbit, checkFor)) {
                                    if (ch == '0') {
                                        eqWithThis = false;
                                        break;
                                    }
                                } else {
                                    if (ch == '1') {
                                        eqWithThis = false;
                                        break;
                                    }
                                }
                            }
                        }
                        if (eqWithThis) {
                            if (then_v !== undefined && then_v != '') {
                                if (if_type == 1) {
                                    temp = process(then_v, data);
                                } else {
                                    temp = my_trim(removeSq(then_v));
                                }
                            } else {
                                if (then_v !== undefined) temp = '';
                            };
                        } else {
                            if (else_v !== undefined && else_v != '') {
                                if (if_type == 1) {
                                    temp = process(else_v, data);
                                } else {
                                    temp = my_trim(removeSq(else_v));
                                }
                            } else {
                                if (else_v !== undefined) temp = '';
                            };
                        }
                    }
                    str = str_replace(j_var[0] + name_var + j_var[1], temp + '', str);
                } else {
                    debug_log('too long or short Value[*..*] in ' + name + ' on ' + str.substr(ind_s, ind_e - (ind_s)));
                    ind_s = ind_s + 1;
                }
            }


            ///parse JSON arrays
            ///parse JSON arrays
            ///parse JSON arrays
            ind_s = 0;
            ind_e = 0;
            var filter = '';
            while (str.indexOf(j_loop[0], ind_s) != -1) {
                crop = -1;
                limits = -1;
                if_type = -1;
                ind_s = str.indexOf(j_loop[0], ind_s);
                ind_e = str.indexOf(j_loop[1], ind_s + j_loop[0].length);
                filter = '';
                set_filter(filter);
                temp_str = '';
                if ((ind_e != -1) && ((ind_e - ind_s) < 195) && ((ind_e - ind_s) > 0)) {
                    name_template = str.substr(ind_s + j_loop[0].length, ind_e - (ind_s + j_loop[0].length));
                    temp_template = name_template.split(',');
                    temp_str = '';

                    var ttt = 2;
                    var pars_new = '';
                    for (ttt = 2; ttt < temp_template.length; ttt++) {
                        pars_new = temp_template[ttt];
                        if (pars_new.indexOf('if=`') != -1) {
                            filter = pars_new;
                            set_filter(filter);
                        } else if (pars_new.indexOf('limit=`') != -1) {
                            limits = parseInt(str_replace('limit=', '', str_replace('`', '', pars_new)));
                            if (limits < 1) {
                                limits = -1;
                            };

                        } else if (pars_new.indexOf('default=`') != -1) {
                            defaults = str_replace('default=', '', str_replace('`', '', pars_new));
                        }
                    }

                    temp_data = data;
                    name_var = temp_template[1];
                    temp_data = get_from_data(data, removeSq(name_var));
                    var k = 0;
                    var ccc = temp_data.length - 1;
                    var pagindex = 0;
                    if (ccc < 0) {
                        temp_str = temp_str + defaults + '';
                        debug_log('No data in this array! ' + name_var);
                    };



                    var key = 0;
                    var elements_arr_length = temp_data.length;
                    var total_elem_arr = elements_arr_length;
                    for (key in temp_data) {
                        elements_arr_length--;
                        //filter
                        if ((limits > 0) && (k >= limits)) {
                            break;
                        };
                        if (!check_filter(temp_data[key])) {
                            continue;
                        };
                        //filter_end

                        if ((temp_data[key] instanceof Object)) {
                            temp_data[key]['j2h_counter'] = k + '';
                            temp_data[key]['j2h_key'] = key + '';
                            //k=parseInt(k);
                            if (k == 0) {
                                temp_data[key]['j2h_first'] = '1';
                            };
                            if (k == ccc) {
                                temp_data[key]['j2h_last'] = '1';
                            };
                            //temp_data[key]['index_0'] = 'unused';
                            //temp_data[key]['index_1'] = 'unused';
                            if (((k + 1) % 2) == 0) {
                                temp_data[key]['j2h_even'] = '1';
                            } else {
                                temp_data[key]['j2h_odd'] = '1';
                            };
                        }

                        temp_str = temp_str + process(temp_template[0], temp_data[key]);

                        k++;
                    }

                    str = str_replace(j_loop[0] + name_template + j_loop[1], temp_str, str);

                } else {
                    debug_log('too long or short Foreach[!..!] in ' + name + ' on ' + str.substr(ind_s, ind_e - (ind_s)));
                    ind_s = ind_s + 1;
                }
            }

            ///parse HTML templates
            ///parse HTML templates
            ///parse HTML templates
            ind_s = 0;
            ind_e = 0;
            while (str.indexOf(j_templ[0], ind_s) != -1) {
                crop = -1;
                if_type = -1;
                ind_s = str.indexOf(j_templ[0], ind_s);
                ind_e = str.indexOf(j_templ[1], ind_s + j_templ[0].length);
                var curData = data;
                if ((ind_e != -1) && ((ind_e - ind_s) < 95) && ((ind_e - ind_s) > 0)) {
                    name_template = str.substr(ind_s + j_templ[0].length, ind_e - (ind_s + j_templ[0].length));
                    var name_template_all = name_template;
                    if (name_template.includes(',')) {
                        name_template = name_template.split(',', 2);
                        var dataindex = name_template[1];
                        name_template = name_template[0];
                        curData = get_from_data(curData, dataindex);
                    }
                    str = str_replace(j_templ[0] + name_template_all + j_templ[1], process(name_template, curData), str);
                } else {
                    debug_log('too long or short template{{..}} in ' + name + ' on ' + str.substr(ind_s, ind_e - (ind_s)));
                    ind_s = ind_s + 1;
                }
            }


            level_parce--;
            str = str_replace('~{', '{', str);
            str = str_replace('~}', '}', str);
            str = str_replace('~[', '[', str);
            str = str_replace('~]', ']', str);
            str = str_replace('~*', '*', str);
            str = str_replace('~!', '!', str);
            if (DEBUG && (error_parcer != '') && (level_parce == 0)) {
                //debug_log('some data is left from datasource \n'+error_parcer);
                error_parcer = '';
            };
            return str;
        }

        //replace substring by another substring
        //usefull for templates
        function str_replace(search, replace, osubject) {
            if (osubject === undefined) return osubject;
            //return osubject.replace(search,replace);//replaced only first simbol - can not be user here
            return osubject.split(search).join(replace);
        }

        //special function for filter
        function str_replace_first(search, replace, osubject, start) {
            var i = osubject.indexOf(search, start);
            if (i == -1) {
                return osubject;
            };
            var temp = [
                osubject.substr(0, i),
                osubject.substr(i + search.length, osubject.length - (i + search.length))
            ]
            return temp[0] + replace + temp[1];
        }

        //trim function - remove first and last spaces
        function my_trim(str) {
            if (str === undefined || str === null) {
                return '';
            };
            var changed = true;
            var controlcount = 5;
            while (changed) {
                controlcount--;
                if (controlcount < 1) break;
                changed = false;
                while (str.charAt(str.length - 1) == " ") {
                    str = str.slice(0, str.length - 1);
                    changed = true;
                }
                while (str.charAt(0) == " ") {
                    str = str.slice(1, str.length);
                    changed = true;
                }
                while (str.charAt(str.length - 1) == "\n") {
                    str = str.slice(0, str.length - 1);
                    changed = true;
                }
                while (str.charAt(0) == "\n") {
                    str = str.slice(1, str.length);
                    changed = true;
                }
                while (str.charAt(str.length - 1) == "\r") {
                    str = str.slice(0, str.length - 1);
                    changed = true;
                }
                while (str.charAt(0) == "\r") {
                    str = str.slice(1, str.length);
                    changed = true;
                }
                while (str.charAt(str.length - 1) == "\t") {
                    str = str.slice(0, str.length - 1);
                    changed = true;
                }
                while (str.charAt(0) == "\t") {
                    str = str.slice(1, str.length);
                    changed = true;
                }
            }
            return str
        }

        function del_dub_space(str) {
            if (str === undefined || str === null) {
                return '';
            };
            str = my_trim(str);
            while (str.indexOf('  ') != -1) {
                str = str_replace('  ', ' ', str);
            }
            return str;
        }

        function debug_log(s) {
            if (DEBUG) {
                console.log('Json2Html: ' + s);
            };
        }

        //for debug
        function printObject(arr, level = 1) {
            var print_red_text = "";
            if (!level) level = 0;
            var level_padding = "";
            for (var j = 0; j < level + 1; j++) level_padding += "    ";
            if (typeof(arr) == 'object') {
                for (var item in arr) {
                    var value = arr[item];
                    if (typeof(value) == 'object') {
                        print_red_text += level_padding + "'" + item + "' :\n";
                        print_red_text += printObject(value, level + 1);
                    } else
                        print_red_text += level_padding + "'" + item + "' => \"" + value + "\"\n";
                }
            } else print_red_text = "===>" + arr + "<===(" + typeof(arr) + ")";
            return print_red_text;
        };

        function getJSON(url, mycallback_func) {
            var mycallback = mycallback_func;
            $.getJSON({
                url: url,
                type: 'GET',
                dataType: 'json',
                contentType: 'application/json',
                success: function(data) {
                    mycallback(data);
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    if (DEBUG) {
                        debug_log('Network: ' + textStatus + "\n" + printObject(errorThrown));
                    }
                    mycallback(JSON.parse('{"error":{"state":true,"title":"Network error","message":"' + str_replace("'", '', str_replace('"', '', textStatus)) + '","code":500}}'));
                }
            });
        }


        function postJSON(url, data, mycallback_func) {
            var mycallback = mycallback_func;
            /*var wrapperdata = {
                'postedData': data
            };*/
            var wrapperdata = data;
            $.post({
                url: url,
                data: JSON.stringify(wrapperdata),
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                success: function(data) {
                    mycallback(data);
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    if (DEBUG) {
                        debug_log(textStatus + "\n" + printObject(errorThrown));
                    }
                    mycallback(JSON.parse('{"error":{"state":true,"title":"Network error","message":"' + str_replace("'", '', str_replace('"', '', textStatus)) + '","code":500}}'));
                }
            });

        }

        var all_templates_loaded = 0;

        function lockTemplateCallback() {
            all_templates_loaded++;
        }

        function unlockTemplateCallback() {
            all_templates_loaded--;
        }

        function normalizeTemplates(arr) {
            for (var item in arr) {
                arr[item] = str_replace(j_var[0] + '  ', j_var[0], arr[item]);
                arr[item] = str_replace(j_var[0] + ' ', j_var[0], arr[item]);
                arr[item] = str_replace(j_loop[0] + '  ', j_loop[0], arr[item]);
                arr[item] = str_replace(j_loop[0] + ' ', j_loop[0], arr[item]);
                arr[item] = str_replace(j_templ[0] + '  ', j_templ[0], arr[item]);
                arr[item] = str_replace(j_templ[0] + ' ', j_templ[0], arr[item]);
                arr[item] = str_replace('  ' + j_var[1], j_var[1], arr[item]);
                arr[item] = str_replace(' ' + j_var[1], j_var[1], arr[item]);
                arr[item] = str_replace('  ' + j_loop[1], j_loop[1], arr[item]);
                arr[item] = str_replace(' ' + j_loop[1], j_loop[1], arr[item]);
                arr[item] = str_replace('  ' + j_templ[1], j_templ[1], arr[item]);
                arr[item] = str_replace(' ' + j_templ[1], j_templ[1], arr[item]);
                arr[item] = str_replace('` then `', '`then`', arr[item]);
                arr[item] = str_replace('` then', '`then', arr[item]);
                arr[item] = str_replace('then `', 'then`', arr[item]);
                arr[item] = str_replace('` else `', '`else`', arr[item]);
                arr[item] = str_replace('` else', '`else', arr[item]);
                arr[item] = str_replace('else `', 'else`', arr[item]);
                arr[item] = str_replace('if = `', 'if=`', arr[item]);
                arr[item] = str_replace('if= `', 'if=`', arr[item]);
                arr[item] = str_replace('if =`', 'if=`', arr[item]);
            }
            return arr;
        }

        function load_template(to_template, url, common_func) {
            if (url === undefined) {
                debug_log('Undefined URL in templates array');
                return;
            }
            all_templates_loaded++; //increace template requests counter
            var myParam = url.substring(url.lastIndexOf('/') + 1);
            myParam = my_trim(myParam.substring(0, myParam.lastIndexOf('.')));
            $.get({
                processData: false,
                url: url,
                success: function(data) {
                    if (data.match(/^ *?NextTemplateName: *?\S{1,100} *?$/m)) {
                        debug_log('File with templates detected: ' + myParam)
                        var temlArr = data.split('NextTemplateName:');
                        var i = 0;
                        for (i = 0; i < temlArr.length; i++) {
                            var nIndex = temlArr[i].indexOf('\n');
                            var tParam = '';
                            var tData = '';
                            if (i > 0) {
                                if (nIndex < 0 || nIndex > 100) {
                                    debug_log('Strange template loaded from file ' + myParam + '. All templates should be starter with line "NextTemplateName: name_of_template"');
                                    debug_log(temlArr[i]);
                                    continue;
                                }
                                tParam = my_trim(temlArr[i].substring(0, nIndex));
                                tData = my_trim(temlArr[i].substring(nIndex + 1));
                            } else {
                                tData = my_trim(temlArr[i]);
                                if (tData.length == 0) {
                                    debug_log('thete is nothing in first "' + myParam + '" of the content ' + i);
                                    continue;
                                }
                                tParam = myParam;
                            }
                            /*var tParam = my_trim(temlArr[i].substring(0, nIndex));
                            var tData = my_trim(temlArr[i].substring(nIndex + 1));*/
                            if (tData.length == 0) {
                                debug_log('thete is nothing in one of the content ' + i);
                                continue;
                            }
                            if (tParam.length == 0) {
                                debug_log('thete is no title in one of the templates ' + i);
                                tParam = myParam;
                            }
                            to_template[tParam] = tData;
                            debug_log('Loaded template ' + tParam + ' from file ' + myParam);
                        }
                    } else {
                        to_template[myParam] = data;
                        debug_log('Loaded file ' + myParam);
                    }

                    all_templates_loaded--; //decrease template requests counter
                    if (all_templates_loaded == 0) common_func(); //sending inital requests
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    if (DEBUG) {
                        debug_log(textStatus + "\n" + printObject(errorThrown));
                    }
                }
            });
        }


        function serializeHtmlForm(formObj) {

            function updatejsonformat(obj, o) {
                var n = o.name,
                    v = o.value;
                if ((/\[.*?\]/).test(n)) {
                    var firstN = n.split('[')[0];
                    var indexes = n.match(/\[.*?\]/g);
                    var c = indexes.length;
                    var numerisArraFinal = n.includes('[]');
                    if (obj[firstN] === undefined) {
                        if (c == 1 && numerisArraFinal) {
                            obj[firstN] = new Array();
                        } else {
                            obj[firstN] = {};
                        }
                    }

                    var i = 0;

                    var curObj = obj[firstN];
                    for (i = 0; i < c; i++) {
                        var index = str_replace('[', '', str_replace(']', '', indexes[i]));
                        if (i == c - 1) {
                            if (index == '') {
                                if ($.isArray(curObj)) {
                                    curObj.push(v)
                                }
                            } else {
                                curObj[index] = v;
                            }
                        } else {
                            if (curObj[index] === undefined) {
                                if ((i == (c - 2)) && numerisArraFinal) {
                                    curObj[index] = new Array();
                                } else {
                                    curObj[index] = {};
                                }
                            }
                            curObj = curObj[index]
                        }
                    }
                } else if (obj[n] === undefined) {
                    obj[n] = v;
                }
            }

            var object = {},
                names = {};
            var sarray = formObj.serializeArray();
            $.each(sarray, function(index, o) {
                updatejsonformat(object, o);
            });
            $(formObj).find('input[type="checkbox"]:not(:checked)').each(function(ind, elem) { //insert all unchecked values too
                updatejsonformat(object, {
                    'name': elem.name,
                    'value': elem.value + '__false'
                }) //value of unchecked elements will be ended with "__false"
            });

            $(formObj).find('input[type="checkbox"]:checked').each(function(ind, elem) { //insert all unchecked values too
                updatejsonformat(object, {
                    'name': elem.name,
                    'value': elem.value
                }) //value of unchecked elements will be ended with "__false"
            });


            $(formObj).find('input[type="checkbox"]:disabled:checked').each(function(ind, elem) { //insert all unchecked values too
                updatejsonformat(object, {
                    'name': elem.name,
                    'value': elem.value
                }) //value of unchecked elements will be ended with "__false"
            });


            return object;
        }
        //add new function to JQuerry object
        //add new function to JQuerry object
        //add new function to JQuerry object
        //add new function to JQuerry object
        $.fn.serializeHtmlForm = function() {
            return serializeHtmlForm(this)
        };

        function isAllTemplatesLoaded() {
            return all_templates_loaded < 1;
        }


        var templates_callback_function = 0;
        var shadow_templates_object = {};

        function shadow_templates_callback() {
            if (!isAllTemplatesLoaded()) return false;
            normalizeTemplates(shadow_templates_object);
            translate(shadow_templates_object);
            templates_callback_function();
        }

        function loadTemplatesArray(arr, func) {
            if (!isAllTemplatesLoaded()) {
                alert('Critical error.\nTrying to load templates before previous templates request is completed');
            }
            var i = 0;
            shadow_templates_object = {};
            templates_callback_function = func;
            lockTemplateCallback();
            for (i = 0; i < arr.length; i++) {
                load_template(shadow_templates_object, arr[i], shadow_templates_callback);
            }
            unlockTemplateCallback();
            shadow_templates_callback();
        }

        //public functions


        /**
         * JS Implementation of MurmurHash3 (r136) (as of May 20, 2011)
         *
         * @author <a href="mailto:gary.court@gmail.com">Gary Court</a>
         * @see http://github.com/garycourt/murmurhash-js
         * @author <a href="mailto:aappleby@gmail.com">Austin Appleby</a>
         * @see http://sites.google.com/site/murmurhash/
         *
         * @param {string} key ASCII only
         * @param {number} seed Positive integer only
         * @return {number} 32-bit positive integer hash
         */

        var murmurSeed = Math.round(((Math.random() * 10000) + 10000));

        function murmurhash3_32_gc(key) {
            var seed = murmurSeed;
            var remainder, bytes, h1, h1b, c1, c1b, c2, c2b, k1, i;

            remainder = key.length & 3; // key.length % 4
            bytes = key.length - remainder;
            h1 = seed;
            c1 = 0xcc9e2d51;
            c2 = 0x1b873593;
            i = 0;

            while (i < bytes) {
                k1 =
                    ((key.charCodeAt(i) & 0xff)) |
                    ((key.charCodeAt(++i) & 0xff) << 8) |
                    ((key.charCodeAt(++i) & 0xff) << 16) |
                    ((key.charCodeAt(++i) & 0xff) << 24);
                ++i;

                k1 = ((((k1 & 0xffff) * c1) + ((((k1 >>> 16) * c1) & 0xffff) << 16))) & 0xffffffff;
                k1 = (k1 << 15) | (k1 >>> 17);
                k1 = ((((k1 & 0xffff) * c2) + ((((k1 >>> 16) * c2) & 0xffff) << 16))) & 0xffffffff;

                h1 ^= k1;
                h1 = (h1 << 13) | (h1 >>> 19);
                h1b = ((((h1 & 0xffff) * 5) + ((((h1 >>> 16) * 5) & 0xffff) << 16))) & 0xffffffff;
                h1 = (((h1b & 0xffff) + 0x6b64) + ((((h1b >>> 16) + 0xe654) & 0xffff) << 16));
            }

            k1 = 0;

            switch (remainder) {
                case 3:
                    k1 ^= (key.charCodeAt(i + 2) & 0xff) << 16;
                case 2:
                    k1 ^= (key.charCodeAt(i + 1) & 0xff) << 8;
                case 1:
                    k1 ^= (key.charCodeAt(i) & 0xff);

                    k1 = (((k1 & 0xffff) * c1) + ((((k1 >>> 16) * c1) & 0xffff) << 16)) & 0xffffffff;
                    k1 = (k1 << 15) | (k1 >>> 17);
                    k1 = (((k1 & 0xffff) * c2) + ((((k1 >>> 16) * c2) & 0xffff) << 16)) & 0xffffffff;
                    h1 ^= k1;
            }

            h1 ^= key.length;

            h1 ^= h1 >>> 16;
            h1 = (((h1 & 0xffff) * 0x85ebca6b) + ((((h1 >>> 16) * 0x85ebca6b) & 0xffff) << 16)) & 0xffffffff;
            h1 ^= h1 >>> 13;
            h1 = ((((h1 & 0xffff) * 0xc2b2ae35) + ((((h1 >>> 16) * 0xc2b2ae35) & 0xffff) << 16))) & 0xffffffff;
            h1 ^= h1 >>> 16;

            return h1 >>> 0;
        }



        var level = 10;

        function translate(obj, keys = []) {
            if (obj === undefined) return '';
            if (obj === null || Number.isInteger(obj)) return obj;
            if ((translation_strings === undefined) || (translation_strings === null) || (!(translation_strings instanceof Object))) return obj;
            if (typeof obj === 'string') {
                return translateString(obj);
            }
            level--;
            if (level < 0) {
                level++;
                alert('Stackoverflow protection triggered');
                level = 10;
                return obj;
            }

            var customKeys = false;
            if (Array.isArray(keys) && (keys.length > 0)) {
                customKeys = true;
            }
            for (var key in obj) {
                if (obj[key] === undefined || obj[key] === null || Number.isInteger(obj[key])) continue;
                if (Array.isArray(obj[key]) || (typeof obj[key]) == 'object') {
                    translate(obj[key], keys)
                } else if (typeof obj[key] === 'string' || obj[key] instanceof String) {
                    if (customKeys) {
                        if (keys.includes(key)) {
                            obj[key] = translateString(obj[key]);
                        }
                    } else {
                        obj[key] = translateString(obj[key]);
                    }
                }
            }
            level++;
            return obj;
        }

        function minStopSimbol(arr, index, str) {
            var i = 0;
            var ch = '';
            var temp = -1;
            var len = str.length;
            for (i = 0; i < 41; i++) {
                temp = index + i;
                if (temp >= len) return len;
                ch = str.charAt(temp);
                if (arr.includes(ch)) {
                    return temp;
                }
            }
            return temp;
        }

        /* json object direct echo to JavaScript */
        var translation_strings = null;

        function setTranslationArray(jsonObject) {
            if (jsonObject === undefined) {
                console.log('Translation array is undefined');
                return;
            }
            translation_strings = jsonObject;
            if (Object.keys(translation_strings).length == 0) {
                translation_strings = null;
            }
        }


        var stopSimbols = [' ', '<', '[', '{', '(', "\n", "\t", "\r", '*', ')', '}', ']', '>', '.', ',', '?', ':', ';', '-', '"', '`', "'", '!', '@', '#', '%', '&', '$', '^', '~', '+', '/', '\\', '='];

        function translateString(str) {
            if (str === undefined) return '';
            if ((translation_strings === undefined) || (translation_strings === null) || (!(translation_strings instanceof Object))) return str;
            var indexEnd = -1;
            var movedIndex = -1;
            var prefix_length = translate_prefix.length;
            var checklen = str.length - (prefix_length + 2);
            if (checklen < 0) return str;
            var key = '';
            var keyLen = 0;
            var index = str.indexOf(translate_prefix);
            var counter_protector = 300;
            while (index != -1) {
                counter_protector--;
                if (counter_protector < 0) {
                    alert('Loop protection: JS template library');
                    return str;
                }
                movedIndex = index + prefix_length;
                indexEnd = minStopSimbol(stopSimbols, movedIndex, str);
                keyLen = indexEnd - movedIndex;
                if (keyLen > 2 || keyLen < 40) {
                    key = str.substr(movedIndex, keyLen);
                    if (translation_strings[key] !== undefined) {
                        str = str.replace(translate_prefix + key, translation_strings[key])
                        index = str.indexOf(translate_prefix, index + 1);
                    } else {
                        console.log('No translation for key: "' + key + '"');
                        index = str.indexOf(translate_prefix, indexEnd);
                    }
                } else {
                    index = str.indexOf(translate_prefix, indexEnd);
                }
            }
            return str
        }

        function setDebug(isDebug) {
            DEBUG = isDebug;
        }

        return {
            process: process, //parse loaded templates with JSON response from server - look documentation
            getJSON: getJSON, //send GET request with calback
            postJSON: postJSON, //send POST request  with calback
            loadTemplatesArray: loadTemplatesArray, //load multi-files templates with callback after all files loaded successfully
            setTranslationArray: setTranslationArray, // set translation array with keys as part of "@str.key" in strings without prefix "@str."
            translate: translate, //if you need to translate JSON object manually. All templates are translated automatically
            printObject: printObject, //for debug to see contend of object. you can use "vardump" keyword - [*variable.vardump*]. If you want to see content in HTML
            setDebug: setDebug, //for console output of all library warnings and errors
            serializeHtmlForm: serializeHtmlForm //extend JQuery.serializeArray() with unchecked checkboxes and arrays. You can use JQuery.serializeHtmlForm()
        }
    }(jQuery));
    var Json2Html = J2H; //alternative name
}