<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <!-- Bootstrap -->
        <link href="static/bootstrap/css/bootstrap.css" rel="stylesheet">
        <link href="static/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
        <link href="static/css/screen.css" rel="stylesheet">

        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.0/jquery.min.js"></script>
        <script src="static/bootstrap/js/bootstrap-dropdown.js"></script>
        <script src="static/bootstrap/js/bootstrap-modal.js"></script>
        <script src="static/bootstrap/js/bootstrap-transition.js"></script>
        <script src="static/bootstrap/js/bootstrap-affix.js"></script>

        <title></title>

        <link rel="icon" type="image/x-icon" href="static/favicon.ico" />

        <script>
            $(function(){
                $('#menu').load('menu.html');
            });
        </script>

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

                        <h2 class="form-signin-heading">Login</h2>

                        <div class="alert alert-error">
                            Usuário não existe
                        </div>
                        
                        <input type="text" class="input-block-level" name="username" id="id_username" placeholder="Username">

                        
                        <input type="password" class="input-block-level" placeholder="Password" name="password">

                        <p><a href="auth_password_reset " title="Forgot my password">Forgot my password</a></p>
                        
                        <button class="btn btn-large btn-primary" type="submit">Login</button>
                    </form>
                </div>
            </div>
        </div>        
    </body>
</html>