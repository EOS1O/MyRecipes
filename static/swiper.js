function main() {

  //testAjax
	function testAjax(){
		console.log("here to test")
		var data = {
			'operation':'news'
		}
		$.ajax({
			type:'POST',
			url:"/",
			data:data,
			success:function (result) {
        var imagesCommon = [];
        result.news_data.map((item,idx)=>{
          imagesCommon.push(item.photo)
        });

        console.log(result,"result")

        var root = document.getElementById("root");

        function appendContainer(text) {
          var container = document.createElement("div");
          container.className = "container";

          root.appendChild(container);

          if (text) {
            var introduce = document.createElement("div");
            introduce.className = "introduce";
            var textNode = document.createTextNode(text);
            introduce.appendChild(textNode);
            container.appendChild(introduce);
          }
          return container;
        }

        var fns = [
          function() {
            // var text = "";
            // var container = appendContainer(text);
            // var awesomeSlider = new AwesomeSlider(imagesCommon, container);

            var text = "";
            var container = appendContainer(text);
    
            var content = result.news_data.map((item,idx)=>{
              return(
                {
                  tagName: "div",
                  attrs: {
                    style:
                      "width:100%; height: 100%;  font-size: 32px; color: #fff;display:flex"
                  },
                  children: [
                    {
                      tagName: "img",
                      attrs: {
                        src: item.photo,
                        style: "width:auto;max-width:60%; max-height:100% ;height: calc(100vh - 400px);border-radius:8px;margin:20px"
                      },
                    },
                    {
                      tagName: "div",
                      attrs: {
                        style:
                          "width:100%; height: 100%; font-size: 14px; color: #696969;margin:20px"
                      },
                      children: [
                        {
                          tagName: "div",
                          attrs: {
                            style:
                              "width:100%; font-size: 14px; color: #696969;margin:20px"
                          },
                          children: [
                            item.description
                          ]
                        },
                        {
                          tagName: "div",
                          attrs: {
                            style:
                              "width:100%; font-size: 14px; color: #696969;margin:20px 0 0 20px"
                          },
                          children: [
                            {
                              tagName: "img",
                              attrs: {
                                src: "https://cdn.5iyin.com/time.svg",
                                style: "width: 20px;height:20px;margin:20px"
                              },
                            },
                            {
                              tagName: "span",
                              attrs: {
                                style: "position:relative;bottom:24px"
                              },
                              children: [
                                item.create_date
                              ]
                            }
                          ]
                        },
                        {
                          tagName: "div",
                          attrs: {
                            style:
                              "width:100%; font-size: 14px; color: #696969;margin:0 0 0 20px"
                          },
                          children: [
                            {
                              tagName: "img",
                              attrs: {
                                src: "https://cdn.5iyin.com/love.svg",
                                style: "width: 20px;height:20px;margin:0 20px 20px 20px"
                              },
                            },
                            {
                              tagName: "span",
                              attrs: {
                                style: "position:relative;bottom:24px"
                              },
                              children: [
                                item.likes
                              ]
                            }
                          ]
                        },
                        
                        {
                          tagName: "div",
                          attrs: {
                            style:
                              "width:100%; font-size: 14px; color: #696969;margin:0 0 0 20px"
                          },
                          children: [
                            {
                              tagName: "div",
                              attrs: {
                                style: "width:100px;margin:0 20px 20px 20px"
                              },
                              children:[
                                "Last Update:"
                              ]
                            },
                            {
                              tagName: "span",
                              attrs: {
                                style: "position:relative;bottom:39px;left:120px"
                              },
                              children: [
                                item.modify_time
                              ]
                            }
                          ]
                        },
                      ]
                    }
                  ]
                }
              )
            });
            var awesomeSlider = new AwesomeSlider(content, container, {
              autoplay: true,
              imageDownloading: imageDownloading(),
              imagePlaceholder: imagePlaceholder()
            });
          },
        ];

        for (var i = 0; i < fns.length; i++) {
          fns[i]();
        }
			},
			error:function(e){
				console.log("No")
			}
		})
	}
  testAjax() 
}



function indicator() {
  var text = "哇哈他";
  var wrap = null;
  return {
    style: function() {
      text = this.options.initIndex + 1 + " / " + this.realLen;
      wrap = document.createElement("div");
      wrap.className = "custom-indicator-wrap";
      var textNode = document.createTextNode(text);
      wrap.appendChild(textNode);
      this.eleCollections.listWrap.appendChild(wrap);
    },

    active: function() {
      text = this.current + " / " + this.realLen;
      wrap.innerText = text;
    }
  };
}

function manual() {
  var previous = document.createElement("div");
  previous.className = "manual-btn manual-previous";

  var next = document.createElement("div");
  next.className = "manual-btn manual-next";

  return {
    previous: previous,
    next: next
  };
}

function imageDownloading() {
  var ele = document.createElement("div");
  ele.className = "image-downloading";
  var text = document.createTextNode("loading...");
  ele.appendChild(text);
  return ele;
}

function imagePlaceholder() {
  var ele = document.createElement("div");
  ele.className = "image-placeholder";
  var text = document.createTextNode("error");
  ele.appendChild(text);
  return ele;
}

function readyGo(func) {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", func);
  } else {
    func();
  }
}

readyGo(main);
