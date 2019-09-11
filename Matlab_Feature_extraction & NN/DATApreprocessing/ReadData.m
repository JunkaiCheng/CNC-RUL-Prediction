clear all
i=1;
for min = 32 : 59
    for sec = 0 : 59
        hour = 15;
        txtname = strcat('Ve450_data_real\data_txt\20190628',num2str(hour,'%.2d'),num2str(min,'%.2d'),num2str(sec,'%.2d'),'.txt')
        %data{i,1}=strcat('20190628',num2str(hour,'%.2d'),num2str(min,'%.2d'),num2str(sec,'%.2d'));
        if(exist(txtname,'file')==0)
            fprintf(strcat(txtname,'\n'))
            data{i,1}=0;
            data{i,2}=0;
        else
            data{i,1}=strcat(num2str(hour,'%.2d'),num2str(min,'%.2d'),num2str(sec,'%.2d'));
            data{i,2}=importdata(txtname);
        end
        i=i+1;
    end
end
for min = 0 : 1
    for sec = 0 : 59
        hour = 16;
        txtname = strcat('Ve450_data_real\data_txt\20190628',num2str(hour,'%.2d'),num2str(min,'%.2d'),num2str(sec,'%.2d'),'.txt')
        %data{i,1}=strcat('20190628',num2str(hour,'%.2d'),num2str(min,'%.2d'),num2str(sec,'%.2d'));
        if(exist(txtname,'file')==0)
            fprintf(strcat(txtname,'\n'))
            data{i,1}=0;
            data{i,2}=0;
        else
            data{i,1}=strcat(num2str(hour,'%.2d'),num2str(min,'%.2d'),num2str(sec,'%.2d'));
            data{i,2}=importdata(txtname);
        end
        i=i+1;
    end
end