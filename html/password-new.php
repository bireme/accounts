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

                        <h2 class="form-signin-heading">New Password</h2>

                        <div class="alert alert-error">
                            Usuário não existe
                        </div>
                        
                        <input type="password" class="input-block-level" placeholder="New Password" name="password">
                        <input type="password" class="input-block-level" placeholder="Confirm New Password" name="password">
                        <button class="btn btn-large btn-primary" type="submit">Login</button>
                    </form>
                </div>
            </div>
        </div>        
    </body>
</html>