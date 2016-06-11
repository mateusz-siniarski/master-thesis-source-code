// CONST- CHANGE ALL THESE TO TELL SOLRSTRAP ABOUT THE LOCATION AND
// STRUCTURE OF YOUR SOLR 

var SERVERROOT = 'http://ocean.idi.ntnu.no:8984/solr/merged-ners-vars/select/'; //SELECT endpoint
var SERVERGEO = 'http://ocean.idi.ntnu.no:8984/solr/geo-locations-coordinates/select/';
var SERVERVAR = 'http://ocean.idi.ntnu.no:8984/solr/variable-changes/select/';
var HITTITLE = 'article_title';                                        //Name of the title field- the heading of each hit
var HITBODY = 'text';                                          //Name of the body field- the teaser text of each hit
var HITSPERPAGE = 20;											//page size- hits per page
var FACET_LIMIT = 20;                                          
var FACETS = ['geo_name_str','geo_placetype_str','species_name','species_rank','variable_text','variable_label'];                       //facet categories
var FACETS_RANGES = [];

var FACETS_TITLES = {'geo_name_str': 'Geographical location',
                    'geo_placetype_str':'Place type',
                    'species_name':'Species',
                    'species_rank':'Taxonomy',
                    'variable_text': 'Variable text',
                    'variable_label': 'Variable type'

                    };  // selective rename facet names for display

var HITID = 'article_id'		// Name of the id field
var HITTEASER = 'article_snippet';	// Name of field to use for teaser
var HITLINK = 'article_url';		// Name of field to use for link


var HL = true;
var HL_FL = 'text';
var HL_SIMPLE_PRE = '<strong>';
var HL_SIMPLE_POST = '</strong>';
var HL_SNIPPETS = 3;

var AUTOSEARCH_DELAY = 1000;

var AUTOCOMPLETE_DEFAULTFIELD = null;

//when the page is loaded- do this
  $(document).ready(function() {
    $('#solrstrap-hits').append('<div offset="0"></div>');
    $('#solrstrap-searchbox').attr('value', getURLParam('q'));
    $('#solrstrap-searchbox').focus();
    //when the searchbox is typed- do this
    $('#solrstrap-searchbox').keyup(keyuphandler);
    if (AUTOCOMPLETE_DEFAULTFIELD) {
      $("#solrstrap-searchbox").autocomplete(
	{minLength: 2, source: autocomplete});
    }
    $('form.navbar-search').submit(handle_submit);
    $(window).bind('hashchange', hashchange);
    $('#solrstrap-searchbox').bind("change", querychange);
    hashchange();
  });

  //jquery plugin allows resultsets to be painted onto any div.
  (function( $ ){
    $.fn.loadSolrResults = function(q, fq, offset) {
      $(this).getSolrResults(q, fq, offset);
    };
  })( jQuery );


  //jquery plugin allows autoloading of next results when scrolling.
  (function( $ ){
    $.fn.loadSolrResultsWhenVisible = function(q, fq, offset) {
     
	 elem = this;
      $(window).scroll(function(event){
        if (isScrolledIntoView(elem) && !$(elem).attr('loaded')) {
          //dont instantsearch and autoload at the same time
          if ($('#solrstrap-searchbox').val() != getURLParam('q')) {
	    handle_submit();
          }
          $(elem).attr('loaded', true);
			var fq = getURLParamArray("fq"); 
          $(elem).getSolrResults(q, fq, offset);
          $(window).unbind('scroll');
        }
      });
    };
  })( jQuery );


  //jquery plugin for takling to solr
  (function( $ ){
    var TEMPLATES = {
    'hitTemplate':Handlebars.compile($("#hit-template").html()),
    'summaryTemplate':Handlebars.compile($("#result-summary-template").html()),
    'navTemplate':Handlebars.compile($("#nav-template").html()),
    'chosenNavTemplate':Handlebars.compile($("#chosen-nav-template").html())
    };
    Handlebars.registerHelper('facet_displayname', function(facetname) {
	return((FACETS_TITLES && FACETS_TITLES.hasOwnProperty(facetname)) ?
	       FACETS_TITLES[facetname] : facetname);
      });
    $.fn.getSolrResults = function(q, fq, offset) {
      var rs = this;
      $(rs).parent().css({ opacity: 0.5 });
      $.ajax({url:SERVERROOT,
	      dataType: 'jsonp',
	      data: buildSearchParams(q, fq, offset), 
	      traditional: true,
	      jsonp: 'json.wrf',
	      success: 
	      function(result){
		// console.log(result);
		//only redraw hits if there are new hits available
		if (result.response.docs.length > 0) {
		  if (offset == 0) {
		    rs.empty();
			deleteMarkers();
		    //strapline that tells you how many hits you got
		    rs.append(TEMPLATES.summaryTemplate({totalresults: result.response.numFound, query: q}));
		    rs.siblings().remove();
		  }
		  //draw the individual hits
		//console.log(fq);
		  for (var i = 0; i < result.response.docs.length; i++) {
		    var hit_data = normalize_hit(result, i);
			
			if('variable_text' in hit_data && 'variable_label' in hit_data)
              hit_data['filtered_vars'] = filterOutVars(hit_data);
			

		    rs.append(TEMPLATES.hitTemplate(hit_data));
		  }
		  	/*
		  	list_geo_names = [];
		  	//if (fq.length > 0) {
		  		var regex = /(.*):"(.*)"/;
				for(i=0;i<fq.length;i++) {
					var match = regex.exec(fq[i]);
					if(match[1] === "geo_name_str") {
						list_geo_names.push(match[2]);
						list_geo_names.push("0");
					}
		  		}
		  		if(list_geo_names.length == 0) {
		  			list_geo_names = result.facet_counts.facet_fields.geo_name_str;
		  		}
		  	/*}
		  	else {*/
			  	list_geo_names = result.facet_counts.facet_fields.geo_name_str;
			/*}*/
			
			for (var j = 0; j < list_geo_names.length; j+=2) {
			geo_name = list_geo_names[j];
			//qconsole.log(geo_name);
			$.ajax({url:SERVERGEO,
	      	dataType: 'jsonp',
	      	data: buildSearchParamsGeo(geo_name), 
	      	traditional: true,
	      	jsonp: 'json.wrf',
	      	success: 
	      	function(result_geo){
				coordinates = result_geo.response.docs[0];
				
                if (coordinates !== undefined) {
                    addMarker(coordinates['geo_name'], coordinates['geo_lat'], coordinates['geo_lng']);
                }
            }
            });
            }


		  $(rs).parent().css({ opacity: 1 });
		  //if more results to come- set up the autoload div
		  if ((+HITSPERPAGE+offset) < +result.response.numFound) {
		    var nextDiv = document.createElement('div');
		    $(nextDiv).attr('offset', +HITSPERPAGE+offset);
		    rs.parent().append(nextDiv);
		    $(nextDiv).loadSolrResultsWhenVisible(q, fq, +HITSPERPAGE+offset);
		  }
		  if (offset === 0) {
		    //facets
		    $('#solrstrap-facets').empty();
		    //chosen facets
		    if (fq.length > 0) {
		      var fqobjs = [];
		      for (var i = 0; i < fq.length; i++) {
			var m = fq[i].match(/^([^:]+):(.*)/);
			if (m) {
			  fqobjs.push({'name': m[1], 'value': m[2]});
			}
		      }
		    }
		    $('#solrstrap-facets').append(TEMPLATES.chosenNavTemplate(fqobjs));
		    //available facets
		    var k;
		    for (k in result.facet_counts.facet_fields) {
		      if (result.facet_counts.facet_fields[k].length > 0) {
			$('#solrstrap-facets')
			  .append(TEMPLATES.navTemplate({
			    title: k,
			    navs:
			    makeNavsSensible(result.facet_counts.facet_fields[k])}));
		      }
		    }
		    for (k in result.facet_counts.facet_ranges) {
		      if (result.facet_counts.facet_ranges[k].counts.length > 0) {
			$('#solrstrap-facets')
			  .append(TEMPLATES.navTemplate({
			    title: k,
			    navs:
			    makeNavsSensible(result.facet_counts.facet_ranges[k].counts)}));
		      }
		    }
		    $('div.facet > a').click(add_nav);
		    $('div.chosen-facet > a').click(del_nav);
		  }}
	      }});
    };
  })( jQuery );


function retrieveLastTokens(text, start, end, length) {
    var chars = text.substring(start,end);
    var tokens = chars.split(' ');
    var counter = 0;
    var subtext = '';
    for(var i=tokens.length-1;i>=0;i--) {
        if (counter > length) {
            break;
        }
        subtext = tokens[i] + ' ' + subtext;
        counter++;
    }
    return subtext+' ';
}

function retrieveFirstTokens(text, start, end, length) {
    var chars = text.substring(start,end);
    var tokens = chars.split(' ');
    var counter = 0;
    var subtext = '';
    for(var i=0;i<tokens.length;i++) {
        if (counter > length) {
            break;
        }
        if(counter == 0) {
            subtext = tokens[i];
        }
        else {
            subtext = subtext + ' ' + tokens[i];
        }
        counter++;
    }
    return ' '+subtext;
}
function filterOutVars(hit_data) {
        var vars_texts = hit_data['variable_text']
        var vars_labels = hit_data['variable_label'].split(',');
        var text = hit_data['text'];

        var fq = getURLParamArray("fq");
        var regex = /(.*):"(.*)"/;
        var filtered_vars = '';

        var offset = 200;
        var q = getURLParam('q').replace(/"/g,'');

            var counter = 0;
            //if facets selected
            for(var i=0;i<fq.length;i++) {
                var match = regex.exec(fq[i]);
                for(var j=0;j<vars_texts.length;j++) {

                    if(match[1] === "variable_label" && match[2] === vars_labels[j]) {
                        counter++;
                        var color = setColor(match[2]);
                        var start_index = -1;
                        var end_index = -1;
                        getCharStartEnd(hit_data,vars_texts[j],function(array) {
                            start_index = array[0];
                            end_index = array[1];
                        });

                        var offsets = getOffsets(start_index,end_index,offset,text.length);
                        var pre_offset = offsets[0];
                        var post_offset = offsets[1];

                        var subtext = text.substring(start_index,end_index);
                        var subtextpre = retrieveLastTokens(text,pre_offset,start_index,10);
                        var subtextpost = retrieveFirstTokens(text,end_index,post_offset,10);
                        if (vars_texts[j].length > 0)
                            //filtered_vars = filtered_vars + '<em><font color="'+color+'">'+vars_texts[j]+'</font></em><br>';
                            var temp_filtered_vars = subtextpre+'<em><font color="'+color+'">'+subtext+'</font></em>'+subtextpost;
                            //if(temp_filtered_vars.toLowerCase().indexOf(q.toLowerCase()) !== -1) {
                                filtered_vars = filtered_vars + subtextpre+'<em><font color="'+color+'">'+subtext+'</font></em>'+subtextpost+'<br><br>';
                            //}

                }

                }
            }
        //if no facets selected
        if (counter === 0) {
            for(var j=0;j<vars_texts.length;j++) {


                var color = setColor(vars_labels[j]);
                var start_index = -1;
                var end_index = -1;
                getCharStartEnd(hit_data,vars_texts[j],function(array) {
                    start_index = array[0];
                    end_index = array[1];
                });

                var offsets = getOffsets(start_index,end_index,offset,text.length);
                var pre_offset = offsets[0];
                var post_offset = offsets[1];

                var subtext = text.substring(start_index,end_index);
                var subtextpre = retrieveLastTokens(text,pre_offset,start_index,10);
                var subtextpost = retrieveFirstTokens(text,end_index,post_offset,10);
                if (vars_texts[j].length > 0)
                //filtered_vars = filtered_vars + '<em><font color="'+color+'">'+vars_texts[j]+'</font></em><br>';
                    var temp_filtered_vars = subtextpre+'<em><font color="'+color+'">'+subtext+'</font></em>'+subtextpost;
                    //if(temp_filtered_vars.toLowerCase().indexOf(q.toLowerCase()) !== -1) {
                        filtered_vars = filtered_vars + subtextpre+'<em><font color="'+color+'">'+subtext+'</font></em>'+subtextpost+'<br><br>';
                    //}
            }
        }

        var filtered_vars = filtered_vars.replace(new RegExp(q,'ig'), function (match) {
            return "<strong>" + match + "</strong>"  ;
        });



        return filtered_vars;
    }

function getAllIndexes(arr, val) {
    var indexes = [], i = -1;
    while ((i = arr.indexOf(val, i+1)) != -1){
        indexes.push(i);
    }
    return indexes;
}

    function getOffsets(start_index,end_index,offset,text_length) {
        var pre_offset = start_index - offset;
        var post_offset = end_index + offset;
        if (pre_offset < 0) {
            pre_offset = 0;
        }
        if (post_offset > text_length) {
            post_offset = text_length
        }
        return [pre_offset, post_offset];
    }


    function setColor(label) {
        var color = '';
        if (label === 'increase') {color = 'red';}
        else if (label === 'decrease') {color = 'blue';}
        else {color = 'green';}
        return color;
    }

  //translates the ropey solr facet format to a more sensible map structure
  function makeNavsSensible (navs) {
    var newNav = {};
    for (var i = 0; i < navs.length; i+=2) {
      newNav[navs[i]] = navs[i + 1];
    }
    return newNav;
  }

  //utility function for grabbling URLs
  function getURLParam(name) {
    var ret = $.bbq.getState(name);
    return ret;
  }

  //function to generate an array of URL parameters, where there are likely to be several params with the same key
  function getURLParamArray(name) {
    var ret =  $.bbq.getState(name) || [];
    if (typeof(ret) == 'string')
      ret = [ret];
    return ret;
  }

  //utility function that checks to see if an element is onscreen
  function isScrolledIntoView(elem) {
    var docViewTop = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();
    var elemTop = $(elem).offset().top;
    var elemBottom = elemTop + $(elem).height();
    return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
  }

  function buildSearchParams(q, fq, offset) {
    if (q === undefined) {
		q = "";
	}
	/*
	if (fq.length > 0) {
		q1 = '(text:"'+q
		q2 = 'text:('+q+')'
		var regex = /(.*):"(.*)"/;
        var count_facets = 0
		for(i=0;i<fq.length;i++) {
			var match = regex.exec(fq[i]);
			if (match[1] !=='geo_placetype_str' && match[1] !=='species_rank' && match[1] !=='variable_label') {
                q1 = q1 + ' '+match[2];
                q2 = q2 +' and '+'&& text:('+match[2]+')'
                count_facets++;
            }
		}
        if (count_facets > 0)
		    q = ' '+q1+'"~10)^2 ('+q2+')';
        else
            q = 'text:('+q+')';
	}
	else {
		q = 'text:('+q+')';
	}*/

      var q_hl = ''
      if (fq.length > 0) {
          var q_no_quotes = q.replace(/"/g,'');
          q1 = '(text:"'+q_no_quotes
          q2 = 'text:('+q+')'
          var regex = /(.*):"(.*)"/;
          var count_facets = 0
          for(i=0;i<fq.length;i++) {
              var match = regex.exec(fq[i]);
              if (match[1] !=='geo_placetype_str' && match[1] !=='species_rank' && match[1] !=='variable_label') {
                  q1 = q1 + ' '+match[2];
                  q2 = q2 +' and '+'&& text:('+match[2]+')'
                  count_facets++;
              }
          }
          if (count_facets > 0)
              q_hl = ' '+q1+'"~10)^2 ||  ('+q2+')';//text:('+q+')';
          else
              q_hl = 'text:('+q+')';
      }
      else {
          q_hl = 'text:('+q+')';
      }
      q = 'text:('+q+')';
	console.log(q)
      console.log(q_hl)
	var ret = { 
    'rows': HITSPERPAGE,
    'wt': 'json',
    'q': q,
	//'q': 'text:"'+q+'"',
    'start': offset
    }
    if (FACETS.length > 0) {
      ret['facet'] = 'true';
	  ret['facet.sort'] = 'count';
      ret['facet.mincount'] = '1';
      //ret['facet.limit'] = '20';
	  ret['facet.limit'] = FACET_LIMIT;
      ret['facet.field'] = FACETS;
    }
    if (FACETS_RANGES) {
      var ranges = [];
      for (facet in FACETS_RANGES) {
	if (FACETS_RANGES.hasOwnProperty(facet)) {
	  ranges.push(facet);
	  var facetdata = FACETS_RANGES[facet];
	  ret['f.'+facet+'.facet.range.start'] = facetdata[0];
	  ret['f.'+facet+'.facet.range.end']= facetdata[1];
	  ret['f.'+facet+'.facet.range.gap']= facetdata[2];
	}
      }
      ret['facet.range'] = ranges;
    }
    if (fq.length > 0) {
      ret['fq'] = fq;
    }
    if (HL_FL) {
      ret['hl'] = 'true';
      ret['hl.q'] =   q_hl;
      ret['hl.fl'] = HL_FL;
      ret['hl.simple.pre'] = HL_SIMPLE_PRE;
      ret['hl.simple.post'] = HL_SIMPLE_POST;
      ret['hl.snippets'] = HL_SNIPPETS;
    }
	console.log(ret);
    return ret;
  }



  function buildSearchParamsGeo(geo_name) {
	var ret = {
    'rows': HITSPERPAGE,
    'wt': 'json',
    'q': 'geo_name:'+geo_name
    }

    return ret;
  }

function buildSearchParamsVar(article_id) {
    var ret = {
        'rows': HITSPERPAGE,
        'wt': 'json',
        'q': 'article_id:'+article_id
    }

    return ret;
}

function buildSearchParamsCharPos(article_id,var_text) {
    var ret = {
        'rows': HITSPERPAGE,
        'wt': 'json',
        'q': 'article_id:"'+article_id+ '"  subStr:"'+var_text+'"'
    }
    console.log(ret);
    return ret;
}

  //optionally convert a string array to a string, by concatenation
  function array_as_string(object)
  {
    if (typeof(object) == 'object' 
	&& object.hasOwnProperty('length') 
	&& object.length > 0) {
      
      //return object.join("; ");
      return object.join();
    }
    return object;
  }

  //normalize a string with respect to whitespace:
  //1) Remove all leadsing and trailing whitespace
  //2) Replace all runs of tab, space and &nbsp; with a single space
  function normalize_ws(object) 
  {
    if (typeof(object) === 'string') {
      return object.replace(/^\s+/, '')
	.replace(/\s+$/, '')
	.replace(/(?: |\t|&nbsp;|&#xa0;|\xa0)+/g, ' ');
    }
    return object;
  }


  //get field from result for document i, optionally replacing with
  //highlit version
  function get_maybe_highlit(result, i, field) 
  {
    var res = result.response.docs[i][field];
    if (HL) {
      var id = result.response.docs[i]['id'];
      var hl_map = result.highlighting[id];
      if (hl_map.hasOwnProperty(field)) {
	res = hl_map[field];
      }
	  else {
	res = ""
	}
    }

    return array_as_string(res);
  }

function get_maybe_highlit_direct(result, i, field, text)
{
    var res = text;
    if (HL) {
        var id = result.response.docs[i]['id'];
        var hl_map = result.highlighting[id];
        if (hl_map.hasOwnProperty(field)) {
            res = hl_map[field];
        }
        else {
            res = ""
        }
    }

    return array_as_string(res);
}

  //handler for navigator selection
  function add_nav(event) 
  {
    var whence = event.target;
    var navname = $(whence).closest("div.facet").children("span.nav-title").data("facetname");
    var navvalue = $(whence).text();
    var newnav = navname + ':"' + navvalue.replace(/([\\\"])/g, "\\$1") + '"';
    var fq = getURLParamArray("fq");

    // check if it already exists...
    var existing = $.grep(fq, function(elt, idx) {
	return elt === newnav;
      });

    if (existing.length === 0) {
      fq.push(newnav);
      $.bbq.pushState({'fq': fq});
    }
    return false;
  }
  
  
  function add_nav_from_pin(geo_name) 
  {
    navname = FACETS[0];
    var newnav = navname + ':"' + geo_name.replace(/([\\\"])/g, "\\$1") + '"';
    var fq = getURLParamArray("fq");

    // check if it already exists...
    var existing = $.grep(fq, function(elt, idx) {
	return elt === newnav;
      });

    if (existing.length === 0) {
      fq.push(newnav);
      $.bbq.pushState({'fq': fq});
      
    }
    else {
    	fq = $.grep(fq, function(elt, idx) {
		return elt === newnav;
      }, true);
    $.bbq.pushState({"fq": fq});
    }
    return false;
  }

  //handler for navigator de-selection
  function del_nav(event) 
  {
    var whence = event.target;
    if ($(whence).hasClass("close")) {
      whence = $(whence).next();
    }
    // var filter = $(whence).text();
    var filter = $(whence).data("filter");    
    var fq = getURLParamArray("fq");

    fq = $.grep(fq, function(elt, idx) {
	return elt === filter;
      }, true);
    $.bbq.pushState({"fq": fq});
    return false;
  }

  function hashchange(event)
  {
    $('#solrstrap-hits div[offset="0"]').loadSolrResults(getURLParam('q'), getURLParamArray('fq'), 0);
  }

  function handle_submit(event)
  {
    var q = $.trim($('#solrstrap-searchbox').val());
    if (q !== '') {
      $.bbq.removeState("fq");
      $.bbq.removeState("q");
      $.bbq.pushState({'q': q});
    }
    return false;
  }

  var querychange = handle_submit;

  var timeoutid;
  function keyuphandler()
  {
    if (AUTOSEARCH_DELAY >= 0) {
      if (timeoutid) {
	window.clearTimeout(timeoutid);
      }
      timeoutid = window.setTimeout(maybe_autosearch, AUTOSEARCH_DELAY);
    }
  }

  function maybe_autosearch()
  {
    if (timeoutid) {
      window.clearTimeout(timeoutid);
    }
    var q = $.trim($('#solrstrap-searchbox').val());
    if (q.length > 3 && q !== getURLParam("q")) {
      $('#solrstrap-hits div[offset="0"]').loadSolrResults(q, [], 0);
    }
    else {
      // $('#solrstrap-hits').css({ opacity: 0.5 });
    }
  }

  function normalize_hit(result, i) {
    var hit_data = $.extend({}, result.response.docs[i]);

    if (result.hasOwnProperty("highlighting")) {
      $.extend(hit_data, result.highlighting[hit_data[HITID]]);
    }

    // hysterical-raisins-are-us: 
    // these mappings are provided for compatibility with code that
    // assumes that the hit data is composed of title, body, link &
    // teaser. it is probably better to use the field names actually
    // returned by SOLR.
    if (HITTITLE || HITLINK || HITBODY || HITTEASER) {
      var aux = {};
      if (HITTITLE) {
	aux.title = hit_data[HITTITLE];
      }
      if (HITLINK) {
	aux.link = hit_data[HITLINK];
      }
      if (HITBODY) {

          aux.text = hit_data[HITBODY]

      }

      if (HITTEASER) {
          /*tmp_text = get_maybe_highlit_direct(result,i,HITBODY,aux.text);

          addVariablesToText(hit_data.article_id, tmp_text,function(new_teaser) {
              hit_data[HITTEASER] = new_teaser;
              aux.teaser = new_teaser;
          });
           */
          tmp_text = get_maybe_highlit_direct(result,i,HITBODY,aux.text);
	        hit_data[HITTEASER] = tmp_text;
          aux.teaser = tmp_text;

      }
      $.extend(hit_data, aux);
    }

    for (k in hit_data) {
      if(k !== 'variable_text') {
          hit_data[k] = normalize_ws(array_as_string(hit_data[k]));
      }
    }

    return hit_data;
  }

function getCharStartEnd(hit_data, var_text,callback) {
    //return '<font color="green">'+teaser+'</font>';
    $.ajax({
        url: SERVERVAR,
        dataType: 'json',
        async: false,
        data: buildSearchParamsCharPos(hit_data['article_id'],var_text),
        traditional: true,
        jsonp: 'json.wrf',
        success: function (result_var) {
            callback([result_var.response.docs[0].charOffsetBegin,result_var.response.docs[0].charOffsetEnd]);
        }
    });
}

    function addVariablesToText(article_id, teaser, callback) {
        //return '<font color="green">'+teaser+'</font>';
        $.ajax({url:SERVERVAR,
            dataType: 'json',
            async: false,
            data: buildSearchParamsVar(article_id),
            traditional: true,
            jsonp: 'json.wrf',
            success:
                function(result_var){

                    data = result_var.response.docs;
                    var new_teaser = teaser;
                    for(i=0;i<data.length;i++) {
                        var variable_change = data[i].subStr;
                        var label = data[i].label;
                        var color = '';
                        if (label === 'increase') {color = 'red';}
                        else if (label === 'decrease') {color = 'blue';}
                        else {color = 'green';}
                        //var re = new RegExp(variable_change,"g");

                        var variable_change_tokens = variable_change.split(' ');
                        var teaser_tokens = new_teaser.replace( /\n/g, " " ).split(" ");

                        if(checkIfContainsPhrase(variable_change_tokens,teaser_tokens)) {
                            new_teaser = markPhrase(variable_change_tokens,teaser_tokens,color)
                        }
                        //else {

                        //}

                    }
                    callback(new_teaser)
                }
        });


    }


    function checkIfContainsPhrase(variable_change_tokens, teaser_tokens) {
        j = 0
        while(j<teaser_tokens.length) {
            var teaser_value = teaser_tokens[j];
            var variable_value = variable_change_tokens[0];
            if (variable_value === 'well') {
                console.log('breakpoint marine')
            }
            if (teaser_value === 'well') {
                console.log('breakpoint marine')
            }

            var index = teaser_value.toLowerCase().indexOf(variable_value.toLowerCase());
            if (index > -1) {
                for(k=1;k<variable_change_tokens.length;k++) {
                    if(j+k<teaser_tokens.length) {
                        var teaser_value = teaser_tokens[j + k];
                        var variable_value = variable_change_tokens[k];
                        index = teaser_value.toLowerCase().indexOf(variable_value.toLowerCase())
                        if (index == -1) return false;
                    }
                }
                return true;
            }
        j++;
        }
        return false;


    }

    function markPhrase(variable_change_tokens, teaser_tokens,color) {
        j = 0
        while(j<teaser_tokens.length) {
            var teaser_value = teaser_tokens[j];
            var variable_value = variable_change_tokens[0];

            var regex_query = /<strong>(.*)<\/strong>/;
            var regex_used = /color=".*">(.*)<\/font>/;

            var teaser_value_string = teaser_value;

            //check if token already used
            var teaser_token_used = regex_used.test(teaser_value);
            var teaser_token_query = regex_query.test(teaser_value);
            if (teaser_token_used === false) {
                if (teaser_token_query) {
                    teaser_value_string =  regex_query.exec(teaser_value)[1];
                }
            }
            else {
                j++;
                continue;
            }

            var index = teaser_value.toLowerCase().indexOf(variable_value.toLowerCase());
            var alreadyMarked = teaser_value.toLowerCase().indexOf('</font></em>');
            if (index > -1 && alreadyMarked == -1) {
            /*if(teaser_value_string.toLowerCase().indexOf(variable_value.toLowerCase())) {*/
                for (k = 0; k < variable_change_tokens.length; k++) {
                    if(j+k<teaser_tokens.length) {
                        var teaser_value = teaser_tokens[j + k];
                        var variable_value = variable_change_tokens[k];
                        teaser_tokens[j+k] = '<em><font color="'+color+'">'+teaser_tokens[j+k]+'</font></em>';
                    }
                }
                j=j+variable_change_tokens.length;
            }
            else {
                j++;
            }

        }
        var new_teaser = teaser_tokens[0];
        for(j=1;j<teaser_tokens.length;j++) {
            new_teaser = new_teaser + " "+teaser_tokens[j];
        }
        return new_teaser

    }




  function autocomplete(request, callback)
  {
    try {
      $.ajax({url:SERVERROOT,
	      dataType: 'jsonp',
	      data: {
		q: "*:*",
		rows: 0,
		wt: "json",
		facet: true,
		'facet.field': AUTOCOMPLETE_DEFAULTFIELD,
		'facet.prefix': request.term,
	      },
	      traditional: true,
	      jsonp: 'json.wrf',
	      // async: false,
	      success: 
	      function(result){
		var completions = [];
		try {
		  var comps = result.facet_counts.facet_fields[AUTOCOMPLETE_DEFAULTFIELD];
		  for (var i = 0; i < comps.length; i+= 2) {
		    completions.push(comps[i]);
		  }
		}
		catch (ex) {
		  alert(ex);
		}
		callback(completions);
	      }});
    }
    catch (ex) {
      alert(ex);
    }    
  }
var map;
  function initMap() {
    var mapDiv = document.getElementById('map');
    map = new google.maps.Map(mapDiv, {
      center: {lat: 58.39124, lng: 18.82117},
      zoom: 3
    });
  }var markers = [];
  function addMarker(title, lat, lng) {
      	var myLatLng = new google.maps.LatLng(lat, lng);
      	
      	for(var x = 0; x < markers.length; x++) {
    		if ( markers[x].getPosition().equals( myLatLng ) ) {
        	//console.log('already exist');
        	return;
    	}
}		
		marker_url = 'http://maps.google.com/mapfiles/ms/micons/blue-dot.png';
		var fq = getURLParamArray("fq");
		var regex = /(.*):"(.*)"/;
				for(i=0;i<fq.length;i++) {
					var match = regex.exec(fq[i]);
					if(match[1] === "geo_name_str" && match[2] === title) {
						marker_url = 'http://maps.google.com/mapfiles/ms/micons/red-dot.png';
						break;
					}
		  		}

      	var marker = new google.maps.Marker({
    	position: {lat: lat, lng: lng},
    	map: map,
    	title: title,
    	icon: marker_url
    	});
    	markers.push(marker);
    	
    	marker.addListener('click', function() {
    		 
    		 add_nav_from_pin(title);
  		});
    	
    }
    function deleteMarkers() {
  		clearMarkers();
  		markers = [];
	}
	
	function clearMarkers() {
  			setMapOnAll(null);
	}
	function setMapOnAll(map) {
  		for (var i = 0; i < markers.length; i++) {
    	markers[i].setMap(map);
  	}
}

   
    
  
  

