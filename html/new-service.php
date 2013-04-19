<!DOCTYPE html>
<html>
    <? include 'head.php' ?>
    <body>
        <div class='mask'><img src='static/image/loading.gif'></div>
        <div class="wrap">
            <? include 'menu.php' ?>

            
            <ul class="breadcrumb">
                <li><a href="#">Home</a> <span class="divider">/</span></li>
                <li><a href="#">Service</a><span class="divider">/</span></li>
                <li class="active">New</li>
            </ul>
            

            <div class="container-fluid content main">
                <!--  header -->
                <div class='header'>
                    <h2><i class='icon-star'></i> Register New Service</h2>
                </div>

                <? include 'help.php' ?>

                <div class='body'>
                    
                    <form>
                        <fieldset>
                            <legend>Service</legend>
                            
                            <div class='field'>
                                <label for="field">Acronym</label>
                                <input type='text'>
                            </div>

                            <div class='field'>
                                <label for="field">Name</label>
                                <input type='text'>
                            </div>
                        </fieldset>
                    </form>

                    <div class="control-panel form-submit">
                        <button class="btn btn-primary btn-large">Submit</button>
                    </div>
                    
                </div>                
            </div>
            <? include 'footer.php' ?>
        </div>
    </body>
</html>