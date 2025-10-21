# Libraries

def template_v1():
    pass

def template_v2():
    pass


def template_v3():
    pass


def template_v4():
    pass


def template_v4(title, subtitle=None, post_url=None):
    """Create HTML template"""
    html = """
        <div>
            <h5> {title}
            <span class="float-end">
                <a href="{post_url}" target="_blank">
                    <i class="fas fa-link"></i>
                </a>
            </span>
            </h5>
            <h6>{w1} {w2} {w3} {w4}</h6>
             <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">Toggle right offcanvas</button>
             <!--<iframe src="https://www.instagram.com/p/CyGDGR3sv7z/"></iframe>-->

            <!--<img src="display_url" style="width:100%; height:100%;">-->
            <!--<img src="data:image/png;base64,{encoded}" style="width:100%; height:100%;">-->
        </div>
    """
    return None

def template_v5(title, subtitle, shortcode):
    """"""
    html = """
        <div>
            <h5> {title} 
            <span class="float-end">
                <a id='post-sidebar-{shortcode}'
                    href="#" type="button" 
                    class='mr-2'
                    data-bs-toggle="offcanvas" 
                    data-bs-target="#offcanvasRight" 
                    aria-controls="offcanvasRight"> 
                    <i class="fas fa-sliders"></i> 
                </a>
                <a id='post-newtab'
                    href="{post_url}" target="_blank"> 
                    <i class="fas fa-link"></i> 
                </a>
            </span>
            </h5> 
            <h6>{subtitle}</h6>
        </div>
    """
    post_url = "https://www.instagram.com/p/%s/" % shortcode
    return html.format(title=title,
        subtitle=subtitle,
        shortcode=shortcode,
        post_url=post_url)