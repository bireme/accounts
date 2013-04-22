<!DOCTYPE html>
<html>
    <head>
        <? include 'head.php' ?>
    </head>
    <body>
        <div class='mask'><img src='static/image/loading.gif'></div>
        <div class="wrap">

            <!-- content -->
            <div class="container-fluid content login">
                <div id="loginForm">
                    <div class="row">                        
                        <div class="logo" id="logo">
                            <h1><a href="" title="Título da App"><span>Título da App</span></a></h1>
                        </div>
                    </div>

                    <form class="form-signin" action="index.html" method="post" name="login">
                        
                        <input type="hidden" name="next" value="submission.views.index " />

                        <h2 class="form-signin-heading">Reset successful</h2>
                        We've e-mailed you instructions for setting your password to the e-mail address
                        you submitted. You should be receiving it shortly.
                    </form>
                </div>
            </div>
        </div>        
    </body>
</html>