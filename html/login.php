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

                    <form class="form-signin" action="index.php" method="post" name="login">
                        
                        <input type="hidden" name="next" value="submission.views.index " />

                        <h2 class="form-signin-heading">Login</h2>

                        <div class="alert alert-error">
                            Usuário não existe
                        </div>
                        
                        <input type="text" class="input-block-level" name="username" id="id_username" placeholder="Username">

                        
                        <input type="password" class="input-block-level" placeholder="Password" name="password">

                        <p><a href="password-reset.php" title="Forgot my password">Forgot my password</a></p>
                        
                        <button class="btn btn-large btn-primary" type="submit">Login</button>
                    </form>
                </div>
            </div>
        </div>        
    </body>
</html>