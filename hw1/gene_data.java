import java.util.*;
import java.io.File;  
import java.io.InputStreamReader;  
import java.io.BufferedReader;  
import java.io.BufferedWriter;  
import java.io.FileInputStream;  
import java.io.FileWriter; 
public class gene_data{
	public static int GENRE = 8;
	public static int COMPOSER = 15;
	public static int LIBRE = 15;
	public static int SINGER = 10;
    public static int ALBUM = 20;
	public static int LANG = 2;
	public static int LEN = 120;
	public static int SCORE = 10;
	public static int PLAYS = 60;
	public static int RELEASE = 16;
	public static int LABEL = 2;
	public static String[] genre = {"Electronic","Electronic","Electronic","Country","Country","Pure","Jazz","Blues","Punk"};
	//public static String[] composers =  {"Coldplay"}
	//public static String[] libres = {"Coldplay",}
	//public static String[] singers = {"Coldplay", "Tanya","Taylor"}
	//public static String[]
	//public static String[] composers =  
	public static void main(String[] args) {
	Random rand = new Random();
	try {
		int[] threshold = new int[]{GENRE,COMPOSER,LIBRE,SINGER,ALBUM,LANG,LEN,SCORE,PLAYS,RELEASE,LABEL};
		File newfile = new File("out.txt");
		newfile.createNewFile();
		BufferedWriter out = new BufferedWriter(new FileWriter(newfile));  
		StringBuilder sb = new StringBuilder();
        for(int i=0; i <105; i++) {
        	String[] tmp = new String[11];
        	for(int j=0;j<threshold.length;j++) {
        		
				int idx = rand.nextInt(threshold[j]);        		
        		switch (j) {
        			
        			case 0:{
        				tmp[j] = genre[idx];
         				break;
        			}

        			case 5: {
        				if(idx ==0) {
        					tmp[j] = "Chinese";
        				} else {
        					tmp[j] = "English";
        				}
        				break;
        			}

        			case 6: {
        				//sb.append(180+rand.nextInt(120)+",");
        				String s = String.valueOf(180+idx);
        				tmp[j] = (s);
        				break;
        			}
        			case 8:{
        				if(tmp[0].equals("Electronic") || tmp[0].equals("Country")&& Integer.valueOf(tmp[7]) >=6) {
        					String s = String.valueOf(idx+15);
        					tmp[j] = s;
        				} else {
        					String s = String.valueOf(idx);
        					tmp[j] = s;
        				}
        				break;
        			}
        			case 9: {
        				String s = String.valueOf(2000+idx);
        				tmp[j] = s;
        				break;
        			}

        			case 10: {
        				//System.out.print(tmp[0]);
        				if((tmp[0].equals("Electronic") || tmp[0].equals("Country")  || Integer.valueOf(tmp[7])>20) && (rand.nextInt(8)>1)) {
        					// if(Integer.valueOf(tmp[9]) >=2010 || rand.nextInt(8)>1) {
        					// 	tmp[j] = "yes";
        					// }  else {
        					// 	tmp[j] = "no";
        					// }
        					
        					tmp[j] = "yes";
        				} else {
        					tmp[j] = "no";
        				}
        				break;
        			}

        			default: {
        				String s = String.valueOf(1+idx);
        				tmp[j] = (s);
        				break;
        			}
        		}
        		
        	}
        	String str = Arrays.toString(tmp);
        	//System.out.println(str);
        	
        	sb.append(str.replaceAll("(\\[)|(\\])| ",""));
        	sb.append("\n");
        }
        out.write(sb.toString());


        out.flush(); // 把缓存区内容压入文件  
        out.close(); // 最后记得关闭文件 
	} catch (Exception e) {
		System.err.println(e);
	}

	}
}
