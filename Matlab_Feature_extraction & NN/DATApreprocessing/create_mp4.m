    % Prepare the new file.
    vidObj = VideoWriter('RUL2.avi');
    open(vidObj);
 
    % Create an animation.

 
        for k = 205:234
            
            fname=strcat('pics/RUL',num2str(k),'.png');

            frame = imread(fname);

            writeVideo(vidObj,frame);

        end
        for i=1:20
                        
            fname=strcat('pics/RUL234.png');

            frame = imread(fname);

            writeVideo(vidObj,frame);
        end
    % Close the file.
    close(vidObj);