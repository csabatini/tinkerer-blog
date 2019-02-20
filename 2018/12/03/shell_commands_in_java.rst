Executing shell commands in Java
================================

I had a project recently that required testing a Spring web application with a CLI tool (`enqueuer <https://github.com/lopidio/enqueuer>`_). Enqueuer is a testing utility that handles many protocols, including HTTP, AMQP, Kafka, and more; I won't go into too much detail about it here.

The success of this test needed to be based on the exit code of the CLI process: zero for success, non-zero for failure.

Using ProcessBuilder
--------------------
My initial approach used ``ProcessBuilder`` from the Java standard library in a test case. The constructor for ``ProcessBuilder`` accepts a list of string tokens for the desired process.

.. code-block:: java
    
    import java.util.List;
    import java.util.ArrayList;
    import java.util.concurrent.TimeUnit;

    import org.junit.Test;

    import static org.junit.Assert.assertEquals;

    public class ProcessTest {

        @Test
        public void processResultTest() {
            // given
            final int SUCCESS_EXIT_VALUE = 0;
            List<String> tokens = new ArrayList<String>(); 
            tokens.add("uname"); 
            tokens.add("-a"); 
            ProcessBuilder builder = new ProcessBuilder(tokens);
            Process process = builder.start();

            // when
            process.waitFor(1000, TimeUnit.MILLISECONDS);

            // then
            assertEquals(SUCCESS_EXIT_VALUE, process.exitValue());
        }
    }

This code works as intended, but I found there's a more concise solution with the ``Runtime`` class. 

Using Runtime
-------------
``Runtime.exec()`` has a method signature that accepts a single string command for the process, and actually, it uses ``ProcessBuilder`` under the hood.

.. code-block:: java
    
    import java.util.concurrent.TimeUnit;

    import org.junit.Test;

    import static org.junit.Assert.assertEquals;

    public class ProcessTest {

        @Test
        public void processResultTest() {
            // given
            final int SUCCESS_EXIT_VALUE = 0;
            Process process = Runtime.getRuntime().exec("uname -a");

            // when
            process.waitFor(1000, TimeUnit.MILLISECONDS);

            // then
            assertEquals(SUCCESS_EXIT_VALUE, process.exitValue());
        }
    }

Using Groovy
------------
Finally, if you're using Groovy instead of plain Java, the `ProcessGroovyMethods <http://docs.groovy-lang.org/docs/groovy-2.4.0/html/api/org/codehaus/groovy/runtime/ProcessGroovyMethods.html>`_ make this task even easier.

.. code-block:: java
    
    import org.junit.Test

    import static org.junit.Assert.assertEquals

    class ProcessTest {

        @Test
        void processResultTest() {
            // given
            final int SUCCESS_EXIT_VALUE = 0
            Process process = "uname -a".execute()

            // when
            process.waitForOrKill(1000)

            // then
            assertEquals(SUCCESS_EXIT_VALUE, process.exitValue())
        }
    }

That sums up what I learned about creating processes in Java and Groovy - thanks for checking out my first code blog!


.. author:: default
.. categories:: none
.. tags:: java, groovy, junit, testing
.. comments::
