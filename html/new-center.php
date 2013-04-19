<!DOCTYPE html>
<html>
    <? include 'head.php' ?>
    <body>
        <div class='mask'><img src='static/image/loading.gif'></div>
        <div class="wrap">
            <? include 'menu.php' ?>

            
            <ul class="breadcrumb">
                <li><a href="#">Home</a> <span class="divider">/</span></li>
                <li><a href="#">Center</a><span class="divider">/</span></li>
                <li class="active">New</li>
            </ul>
            

            <div class="container-fluid content main">
                <!--  header -->
                <div class='header'>
                    <h2><i class='icon-globe'></i> Register New Center</h2>
                </div>

                <? include 'help.php' ?>

                <div class='body'>
                    
                    <form>
                        <fieldset>
                            <legend>Center</legend>
                            
                            <div class='field'>
                                <label for="field">Country</label>
                                <select>
                                    <option>Brasil</option>
                                    <option>Argentina</option>
                                    <option>EUA</option>
                                </select>
                            </div>

                            <div class='field'>
                                <label for="field">Code</label>
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