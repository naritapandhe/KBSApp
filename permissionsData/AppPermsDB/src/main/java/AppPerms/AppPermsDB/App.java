package AppPerms.AppPermsDB;

/**
 * Hello world!
 *
 */
import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;

import org.neo4j.graphdb.DynamicLabel;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Label;
import org.neo4j.graphdb.Relationship;
import org.neo4j.graphdb.ResourceIterable;
import org.neo4j.graphdb.ResourceIterator;
import org.neo4j.graphdb.Transaction;
import org.neo4j.graphdb.factory.*;
import org.neo4j.graphdb.Transaction;
import org.neo4j.graphdb.Node;
import org.neo4j.graphdb.RelationshipType;



public class App 
{

	private static enum RelTypes implements RelationshipType
	{
	    KNOWS, MY_RELATION, USES_PERMISSION
	}
	
    public static void main( String[] args )
    {
    	//final File DB_PATH=new File("/Users/admin/Desktop/KBS/neoTest/testeroo.db");
    	final File DB_PATH = new File("/Users/admin/Desktop/KBS/googlePlayDB1-Jan2014/googlePlayDB1-Jan2014");
    	//GraphDatabaseService graphDb;
    	Node firstNode;
    	Node secondNode;
    	Relationship relationship;
    	
    	//graphDb = new GraphDatabaseFactory().newEmbeddedDatabase(DB_PATH).
    	GraphDatabaseService graphDb = new GraphDatabaseFactory()
        .newEmbeddedDatabaseBuilder(DB_PATH)
        .loadPropertiesFromFile("/Users/admin/Desktop/KBS/googlePlayDB1-Jan2014/.conf/neo4j.properties")
        .newGraphDatabase();
    	
    	
    	try ( Transaction tx = graphDb.beginTx() )
    	{
    		//Label label = DynamicLabel.label( "APP" );
    		ResourceIterable<Relationship> relationships = graphDb.getAllRelationships();
    		HashMap<String, ArrayList<String>> hm = new HashMap();
    		ArrayList<String> existingPermissions;
    		for(Relationship r : relationships)
            {
    			
                if (r.isType(RelTypes.USES_PERMISSION))
                {
                	//String appName=(String) r.getStartNode().getProperty("name");
                	String appPackage=(String) r.getStartNode().getProperty("package");
                	String permissionName=(String)r.getEndNode().getProperty("name");
                	if(hm.containsKey(appPackage)){
                		existingPermissions=((ArrayList<String>)hm.get(appPackage));
                		existingPermissions.add(permissionName);
                	}else{
                		ArrayList<String> newPermissions = new ArrayList<String>();
                		newPermissions.add(permissionName);
                		hm.put(appPackage, newPermissions);
                	}
                	
                }
                
            }
    		
    		for (String name: hm.keySet()){

                String key =name.toString();
                String value = hm.get(name).toString();  
                System.out.println(key + "," + value);  


    		}
    		

    		/*firstNode = graphDb.createNode();
    		firstNode.setProperty( "message", "Hello " );
    		secondNode = graphDb.createNode();
    		secondNode.setProperty( "message", "World!" );

    		relationship = firstNode.createRelationshipTo( secondNode, RelTypes.KNOWS );
    		relationship.setProperty( "message", "brave Neo4j " );
    		
    		System.out.println("");
    		System.out.print( firstNode.getProperty( "message" )+" -> " );
    		System.out.print( relationship.getProperty( "message")+" -> ");
    		System.out.print( secondNode.getProperty( "message" ) );*/
    		
    	    // Database operations go here
    	    tx.success();
    	}catch(Exception e){
    		e.printStackTrace();
    	}finally{
    		graphDb.shutdown();
    	}
		System.out.println("\nDone successfully!");
    
    }
}
